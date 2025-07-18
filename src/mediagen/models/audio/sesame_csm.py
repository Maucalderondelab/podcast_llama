import time
import asyncio

from ..model_manager import TTSModel

from typing import Any, override

__all__ = [
    "ElevenLabsModelAPI",
]

class ElevenLabsModelAPI(TTSModel):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._client = None
        self._loading_lock = asyncio.Lock()
    
    @override
    async def load(self) -> None:
        async with self._loading_lock:
            if self._client is None:
                # Import only when needed
                from elevenlabs import ElevenLabs
                self._client = ElevenLabs(api_key=self.api_key)
    
    @override
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
