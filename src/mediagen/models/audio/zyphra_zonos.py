# src/mediagen/models/audio/zyphra_zonos.py
import asyncio

import torch
import torchaudio

from mediagen.tts.tts_utils import Audio
from ..model_manager import TTSModel

from typing import override
from pathlib import Path

__all__ = [
    "ZonosModelLocal",
]

class ZonosModelLocal(TTSModel):
    def __init__(self, model_name: str = "Zyphra/Zonos-v0.1-transformer"):
        self.model_name: str = model_name
        self.device: torch.device = self._get_device()
        self._client = None
        self._loading_lock = asyncio.Lock()
    
    def _get_device(self) -> torch.device:
        if torch.cuda.is_available():
            return torch.device(torch.cuda.current_device())
        return torch.device("cpu")
    
    @override
    async def load(self) -> None:
        async with self._loading_lock:
            if self._client is None:
                # Import only when needed
                from zonos.model import Zonos
                
                # TEST: if converting to str fixes the forward NotImplementedError
                device_str: str = str(self.device)

                # Run in thread pool to avoid blocking
                self._client = await asyncio.to_thread(
                    Zonos.from_pretrained,
                    self.model_name,
                    device=device_str
                )

    @override
    def unload(self) -> None:
        if self._client is not None:
            del self._client
            self._client = None
            torch.cuda.empty_cache()
    
    @property
    @override
    def is_loaded(self) -> bool:
        return self._client is not None
    
    @property
    def client(self):
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call await model.load() first.")
        return self._client

    @override
    def prep_speaker(self, audio_path: Path | str) -> torch.Tensor:
        # Lightweight properties - computed when needed
        self.audio_path: Path = Path(audio_path)
        self._speaker_embedding: torch.Tensor | None = self._create_speaker_embedding()
        return self._speaker_embedding
    
    # >>> helper functions for prep_speaker >>>
    def _create_speaker_embedding(self) -> torch.Tensor:
        if not self.audio_path.exists():
            raise FileNotFoundError(f"Voice artist audio not found: {self.audio_path}")
        
        # Load and embed voice sample
        voice = Audio(*torchaudio.load(self.audio_path))
        embedding: torch.Tensor = self.client.make_speaker_embedding(voice.wavtensor, voice.srate)
        torch.cuda.empty_cache()
        return embedding
    # <<< helper functions for prep_speaker <<<

    @property
    def speaker_embedding(self) -> torch.Tensor:
        """Get cached speaker embedding"""
        if self._speaker_embedding is None:
            raise RuntimeError("Speaker not prepared. Call prep_speaker() from ModelManager first")
        return self._speaker_embedding
    
    @override
    def run_speaker(self, text: str) -> Audio:
        # Import conditioning function
        from zonos.conditioning import make_cond_dict

        # prepare model and embed voice
        if self._speaker_embedding is None:
            self.prep_speaker(self.audio_path)

        # Generate audio using shared model
        cond_dict: dict = make_cond_dict(text=text, speaker=self.speaker_embedding)
        conditioning = self.client.prepare_conditioning(cond_dict)
        codes = self.client.generate(conditioning)
        wavs = self.client.autoencoder.decode(codes).cpu()
        
        voice = Audio(wavs[0], self.client.autoencoder.sampling_rate)
        return voice
        

