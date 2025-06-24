import asyncio

import torch

from typing import Any
from abc import ABC, abstractmethod

__all__ = [
    "TTSModel",
    "ModelManager",
    "ZonosModel", 
    "ElevenLabsModel",
]

class TTSModel(ABC):
    """Abstract base class for TTS models"""
    
    @abstractmethod
    async def load(self) -> None:
        """Load the model asynchronously"""
        pass
    
    @abstractmethod
    def unload(self) -> None:
        """Unload model and free memory"""
        pass
    
    @property
    @abstractmethod
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        pass

class ZonosModel(TTSModel):
    def __init__(self, model_name: str = "Zyphra/Zonos-v0.1-transformer"):
        self.model_name = model_name
        self.device = self._get_device()
        self._model = None
        self._loading_lock = asyncio.Lock()
    
    def _get_device(self) -> torch.device:
        if torch.cuda.is_available():
            return torch.device(torch.cuda.current_device())
        return torch.device("cpu")
    
    async def load(self) -> None:
        async with self._loading_lock:
            if self._model is None:
                # Import only when needed
                from zonos.model import Zonos
                
                # Run in thread pool to avoid blocking
                self._model = await asyncio.to_thread(
                    Zonos.from_pretrained, 
                    self.model_name, 
                    device=self.device
                )
    
    def unload(self) -> None:
        if self._model is not None:
            del self._model
            self._model = None
            torch.cuda.empty_cache()
    
    @property
    def is_loaded(self) -> bool:
        return self._model is not None
    
    @property
    def model(self):
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call await model.load() first.")
        return self._model

class ElevenLabsModel(TTSModel):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._client = None
        self._loading_lock = asyncio.Lock()
    
    async def load(self) -> None:
        async with self._loading_lock:
            if self._client is None:
                # Import only when needed
                from elevenlabs import ElevenLabs
                self._client = ElevenLabs(api_key=self.api_key)
    
    def unload(self) -> None:
        self._client = None
    
    @property
    def is_loaded(self) -> bool:
        return self._client is not None
    
    @property
    def client(self):
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call await model.load() first.")
        return self._client

class ModelManager:
    """Singleton model manager for all TTS models"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.models: dict[str, dict[str, TTSModel]] = {
                "tts": {},
                "video": {},
                "image": {}
            }
            self._loading_tasks: dict[str, asyncio.Task] = {}
            ModelManager._initialized = True
    
    def register_model(self, category: str, name: str, model: TTSModel) -> None:
        """Register a model with the manager"""
        if category not in self.models:
            self.models[category] = {}
        self.models[category][name] = model
    
    async def load_model(self, category: str, name: str) -> TTSModel:
        """Load a model asynchronously with deduplication"""
        key = f"{category}_{name}"
        
        if key in self._loading_tasks:
            # Model is already being loaded, wait for it
            await self._loading_tasks[key]
        else:
            model = self.get_model(category, name)
            if not model.is_loaded:
                # Start loading task
                self._loading_tasks[key] = asyncio.create_task(model.load())
                await self._loading_tasks[key]
                # Clean up completed task
                del self._loading_tasks[key]
        
        return self.get_model(category, name)
    
    def get_model(self, category: str, name: str) -> TTSModel:
        """Get a model (must be loaded first)"""
        if category not in self.models or name not in self.models[category]:
            raise ValueError(f"Model {category}/{name} not registered")
        return self.models[category][name]
    
    def unload_model(self, category: str, name: str) -> None:
        """Unload a specific model"""
        model = self.get_model(category, name)
        model.unload()
    
    def unload_category(self, category: str) -> None:
        """Unload all models in a category"""
        if category in self.models:
            for model in self.models[category].values():
                model.unload()
    
    def unload_all(self) -> None:
        """Unload all models"""
        for category in self.models:
            self.unload_category(category)
    
    def get_memory_usage(self) -> dict[str, Any]:
        """Get memory usage info"""
        usage = {}
        for category, models in self.models.items():
            usage[category] = {}
            for name, model in models.items():
                usage[category][name] = {
                    "loaded": model.is_loaded,
                    "type": type(model).__name__
                }
        
        if torch.cuda.is_available():
            usage["gpu_memory"] = {
                "allocated": torch.cuda.memory_allocated(),
                "reserved": torch.cuda.memory_reserved()
            }
        
        return usage


