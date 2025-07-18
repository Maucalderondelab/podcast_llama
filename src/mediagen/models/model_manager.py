# src/mediagen/models/model_manager.py
import asyncio
import time

import torch

from mediagen.tts.tts_utils import Audio

from typing import Any
from abc import ABC, abstractmethod
from pathlib import Path

__all__ = [
    "TTSModel",
    "ModelManager",
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

    @abstractmethod
    def prep_model(self, voice_id: str) -> torch.Tensor:
        """Prep TTS model. Embed a voice sample for either a local or API tts call"""
        pass

    @abstractmethod
    def run_model(self, voice_id: str, text: str) -> Audio:
        """Run TTS model either with an API or locally"""
        pass

# >>> ModelManager >>>
# HACK: ModelManager is a must-have intermediary to load TTS models
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
                "audio": {},
                "video": {},
                "image": {}
            }
            self._loading_tasks: dict[str, asyncio.Task] = {} # NOTE: check type of asyncio.Task
            ModelManager._initialized = True
    
    def register_model(self, category: str, model_name: str, model: TTSModel) -> None:
        """Register a model with the manager"""
        if category not in self.models:
            self.models[category] = {}
        self.models[category][model_name] = model

    def is_registered(self, category: str, model_name: str) -> bool:
        if category not in self.models or model_name not in self.models[category]:
            return False
        return True
    
    async def load_model(self, category: str, model_name: str) -> TTSModel:
        """Load a model asynchronously with deduplication"""
        key = f"{category}_{model_name}"
        
        if key in self._loading_tasks:
            # Model is already being loaded, wait for it
            t0 = time.time()
            await self._loading_tasks[key]
            tf = time.time()
            print(f"Model `{model_name}` cached (took {tf-t0}s)")
        else:
            model = self.get_model(category, model_name)
            if not model.is_loaded:
                # Start loading task
                self._loading_tasks[key] = asyncio.create_task(model.load())
                await self._loading_tasks[key]
                # Clean up completed task
                del self._loading_tasks[key]
        
        return self.get_model(category, model_name)
    
    def get_model(self, category: str, model_name: str) -> TTSModel:
        """Get a model (must be loaded first)"""
        if category not in self.models or model_name not in self.models[category]:
            raise ValueError(f"Model {category}/{model_name} not registered")
        return self.models[category][model_name]
    
    # TODO: all unloads must be tested 
    def unload_model(self, category: str, model_name: str) -> None:
        """Unload a specific model"""
        model = self.get_model(category, model_name)
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

    # >>> prep & run TTSModel >>>
    def prep_speaker(self, model_name: str, voice_id: str) -> torch.Tensor:
        category: str = "audio"
        model = self.get_model(category, model_name)
        return model.prep_model(voice_id=voice_id)

    def run_speaker(self, model_name: str, voice_id: str, text: str) -> Audio:
        category: str = "audio"
        model = self.get_model(category, model_name)
        return model.run_model(voice_id=voice_id, text=text)
    # <<< prep & run TTSModel <<<
    
    # PERF: tested, works nice
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
# <<< ModelManager <<<

