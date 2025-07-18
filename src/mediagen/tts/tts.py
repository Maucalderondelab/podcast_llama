import torch
from torchaudio import load as _torchaudioLoad

from .tts_utils import Audio, save_to_path, torch_concat

from mediagen.models import ModelManager, VOICE_ARTISTS

from dataclasses import dataclass
from pathlib import Path

__all__ = [
    "Speaker", 
    "SpeakerText",
]

@dataclass
class SpeakerText:
    speaker: "Speaker"
    text: str

class Speaker:
    """Speaker class instantiates a voice based on a sample."""
    def __init__(self, mm: ModelManager, model_name: str, voice_artist_name: str):
        self.mm: ModelManager = mm
        self.category: str = "audio"
        self.model_name: str = model_name
        self.speaker_embedding: torch.Tensor | None = None
        self.audio_path: Path = VOICE_ARTISTS[voice_artist_name]
        self.voice_artist_name: str = voice_artist_name
        
        # Lightweight properties - computed when needed
        self.model_manager: ModelManager = mm
    
    # @property
    # def prepare_speaker(self) -> torch.Tensor | None:
    #     self.speaker_embedding: torch.Tensor | None = self.mm.prep_speaker(self.category, self.model_name, self.audio_path)
    #     """Get the shared model instance"""
    #     # Verify that model is reqgistered and loaded
    #     if not self.model_manager.is_registered(self.category, self.model_name):
    #         print(f"Registering category: {self.category} and model_name: {self.model_name}")
    #         self.model_manager.register_model(self.category, self.model_name, )
    
    # NOTE: think if passing an `output_path` is a good system for audio saving
    def speak(
        self,
        text: str,
        output_path: Path | str | None = None,
        dir_path: Path | str | None = None,
        fname: str | None = None,
        save_to_cache: bool = False,
        parents: bool = False,
        exist_ok: bool = True,
    ) -> Audio:
        """Generate speech using the shared model"""
        if not self.model.is_loaded:
            raise RuntimeError(f"Model {self.model_name} not loaded. Load it first with ModelManager.")
        
        # Import only when needed
        from zonos.conditioning import make_cond_dict
        
        # Generate audio using shared model
        cond_dict: dict = make_cond_dict(text=text, speaker=self.speaker_embedding)
        conditioning = self.model.model.prepare_conditioning(cond_dict)
        codes = self.model.model.generate(conditioning)
        wavs = self.model.model.autoencoder.decode(codes).cpu()
        
        voice = Audio(wavs[0], self.model.model.autoencoder.sampling_rate)
        
        # TODO: saving path/fname is not optimal
        # implement saving w/ `save_to_path`
        if output_path is not None or dir_path is not None or fname is not None:
            save_to_path(
                voice,
                output_path, 
                dir_path, 
                fname, 
                save_to_cache, 
                parents, 
                exist_ok,
            )
        
        torch.cuda.empty_cache()
        return voice
