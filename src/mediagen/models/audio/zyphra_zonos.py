# src/mediagen/models/audio/zyphra_zonos.py
import asyncio

import torch
from torchaudio import load as _torchaudioLoad

from .voices import VOICE_ARTISTS
from ..model_manager import TTSModel
from mediagen.tts.tts_utils import Audio

from typing import override, Any
from pathlib import Path

__all__ = [
    "ZonosModelLocal",
]

class ZonosModelLocal(TTSModel):
    def __init__(self, model_name: str = "Zyphra/Zonos-v0.1-transformer"):
        self.model_name: str = model_name
        self.device: torch.device = self._get_device()
        self.speaker_embeddings: dict[str, torch.Tensor] = {}
        self._zonos_model: Any = None
        self._loading_lock = asyncio.Lock()

    def _get_device(self) -> torch.device:
        if torch.cuda.is_available():
            return torch.device(torch.cuda.current_device())
        return torch.device("cpu")
    
    @override
    async def load(self) -> None:
        async with self._loading_lock:
            if self._zonos_model is None:
                # Import only when needed
                from zonos.model import Zonos
                
                # HACK: converting to str fixes the forward NotImplementedError in asyncio.to_thread()
                # In `zonos/model.py`, device argument type hint is marked as str but should be torch.device
                device_str: str = str(self.device)

                # Run in thread pool to avoid blocking
                self._zonos_model = await asyncio.to_thread(
                    Zonos.from_pretrained,
                    self.model_name,
                    device=device_str
                )

    @override
    def unload(self) -> None:
        if self._zonos_model is not None:
            del self._zonos_model
            self._zonos_model = None
            torch.cuda.empty_cache()
    
    @property
    @override
    def is_loaded(self) -> bool:
        return self._zonos_model is not None
    
    @property
    def zonos_model(self):
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call await model.load() first.")
        return self._zonos_model

    @override
    def prep_model(self, voice_id: str) -> torch.Tensor:
        # Lightweight properties - computed when needed
        self.speaker_embeddings[voice_id] = self._create_speaker_embedding(voice_id)
        return self.speaker_embeddings[voice_id]
    
    # >>> helper functions for prep_model >>>
    def _create_speaker_embedding(self, voice_id: str) -> torch.Tensor:
        audio_path: Path = VOICE_ARTISTS[voice_id]
        if not audio_path.exists():
            raise FileNotFoundError(f"Voice artist audio ID {voice_id} not found at path: {audio_path}")

        # Check if embedding for a particualr voice already exists
        if voice_id in self.speaker_embeddings.keys():
            return self.speaker_embeddings[voice_id]
        else:
            # Load and embed voice sample
            voice: Audio = Audio(*_torchaudioLoad(audio_path))
            embedding: torch.Tensor = self.zonos_model.make_speaker_embedding(voice.wavtensor, voice.srate)
            torch.cuda.empty_cache() # TODO: validate if empty_cache is useful here
            return embedding

    def _get_speaker_embedding(self, voice_id: str) -> torch.Tensor:
        """Get cached speaker embedding"""
        if voice_id not in self.speaker_embeddings.keys():
            raise RuntimeError("Speaker not prepared. Call `prep_model()` from `ModelManager().prep_speaker()` first")
        return self.speaker_embeddings[voice_id]
    # <<< helper functions for prep_model <<<
    
    @override
    def run_model(self, voice_id: str, text: str) -> Audio:
        """Access a speaker_embedding and produce audio for the desired text"""
        # Import conditioning function
        from zonos.conditioning import make_cond_dict

        # Generate audio using shared model
        cond_dict: dict[str, Any] = make_cond_dict(text=text, speaker=self._get_speaker_embedding(voice_id))
        conditioning: torch.Tensor = self.zonos_model.prepare_conditioning(cond_dict)
        codes = self.zonos_model.generate(conditioning)
        wavs: torch.Tensor = self.zonos_model.autoencoder.decode(codes).cpu()
        
        voice = Audio(wavs[0], self.zonos_model.autoencoder.sampling_rate)
        return voice
        

