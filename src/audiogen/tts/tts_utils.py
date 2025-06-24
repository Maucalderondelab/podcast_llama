import torch
import torchaudio

from audiogen.models import ModelManager
from audiogen.models import VOICE_ARTISTS

from pathlib import Path
from dataclasses import dataclass
import warnings

__all__ = [
    "Audio",
    "Speaker", 
    "SpeakerText",
    "torch_concat",
    "save_to_path",
]

@dataclass
class Audio:
    wavtensor: torch.Tensor
    srate: int

@dataclass
class SpeakerText:
    speaker: "Speaker"
    text: str


class Speaker:
    """Speaker class instntiates a voice based on a sample."""
    
    def __init__(self, model_name: str, voice_artist_name: str):
        self.model_name = model_name
        self.voice_artist_name = voice_artist_name
        self.audio_path: Path = VOICE_ARTISTS[voice_artist_name]
        
        # Lightweight properties - computed when needed
        self._speaker_embedding: torch.Tensor | None = None
        self._model_manager = ModelManager()
    
    @property
    def model(self):
        """Get the shared model instance"""
        return self._model_manager.get_model("tts", self.model_name)
    
    @property
    def speaker_embedding(self) -> torch.Tensor:
        """Lazy load speaker embedding"""
        if self._speaker_embedding is None:
            self._speaker_embedding = self._create_speaker_embedding()
        return self._speaker_embedding
    
    def _create_speaker_embedding(self) -> torch.Tensor:
        if not self.audio_path.exists():
            raise FileNotFoundError(f"Voice artist audio not found: {self.audio_path}")
        
        # Load and embed voice sample
        voice = Audio(*torchaudio.load(self.audio_path))
        embedding = self.model.model.make_speaker_embedding(voice.wavtensor, voice.srate)
        torch.cuda.empty_cache()
        return embedding
    
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
        cond_dict = make_cond_dict(text=text, speaker=self.speaker_embedding)
        conditioning = self.model.model.prepare_conditioning(cond_dict)
        codes = self.model.model.generate(conditioning)
        wavs = self.model.model.autoencoder.decode(codes).cpu()
        
        voice = Audio(wavs[0], self.model.model.autoencoder.sampling_rate)
        
        # Handle saving if requested
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

def torch_concat(
    audio_segments: list[Audio],
    output_path: Path | str | None = None,
) -> Audio:
    tensors = [seg.wavtensor for seg in audio_segments]
    concatenated = torch.cat(tensors, dim=1)
    sample_rate = audio_segments[0].srate
    
    if output_path:
        torchaudio.save(Path(output_path), concatenated, sample_rate)
    
    return Audio(concatenated, sample_rate)

def save_to_path(
    voice: Audio,
    output_path: Path | str | None = None,
    dir_path: Path | str | None = None,
    fname: str | None = None,
    save_to_cache: bool = False,
    parents: bool = True,
    exist_ok: bool = False,
):
    # Fix the assertion logic - should check if suffix IS in the list
    if output_path is not None:
        assert Path(output_path).suffix in [".mp3", ".wav"], "`output_path` must end with a valid audio file extension."
    if fname is not None:
        assert Path(fname).suffix in [".mp3", ".wav"], "`fname` must end with a valid audio file extension."

    data_path: Path = Path("..", "..", "..", "data")

    # Validate inputs are correct
    if output_path is not None:
        if dir_path is not None or fname is not None:
            warnings.warn("`output_path` provided, ignoring `dir_path` and `fname`.", UserWarning)
        full_path_file: Path = data_path / output_path
    else:
        if dir_path is None or fname is None:
            raise ValueError("Provide either `output_path` or both `dir_path` and `fname`")
        else:
            if save_to_cache:
                full_path: Path = data_path / dir_path / "cache" 
                full_path.mkdir(parents=parents, exist_ok=exist_ok)
                full_path_file: Path = full_path / fname
            else:
                full_path: Path = data_path / dir_path
                full_path.mkdir(parents=parents, exist_ok=exist_ok)
                full_path_file: Path = full_path / fname

    # Fix the torch.save call - should be torchaudio.save
    torchaudio.save(full_path_file, voice.wavtensor, voice.srate)

    _print_output = f"Audio file saved at: {full_path_file}"
    print(_print_output)
    print(len(_print_output) * "-")
