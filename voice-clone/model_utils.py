import torch
import torchaudio
from zonos.model import Zonos
from zonos.conditioning import make_cond_dict
from zonos.utils import DEFAULT_DEVICE

from pathlib import Path

# Default models and speaker voice
DEFAULT_ZONOS_MODEL = Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer", device=DEFAULT_DEVICE)
DEFAULT_MODEL_FILE_PATH = Path("tests") / "kratos-take-00-normCompress.mp3"

# voice artists
VOICE_ARTISTS = {
    "default": "kratos-take-00-normCompress.mp3",
    "british-01": "british-woman-monologue-01.mp3",
    "british-02": "british-woman-monologue-02.mp3",
    "meditation": "meditation-voiceover.mp3",
    "novel": "novel-story-narration.mp3",
    "sports": "SJohnsonVoiceOvers.mp3",
    "western": "western-woman-narration.mp3",
}

# WIP Speakers available
class Speaker:
    def __init__(
        self,
        voice_artist_name: str,
        **kwargs,
    ):
        self.audio_path: Path = Path("tests") / VOICE_ARTISTS[voice_artist_name]

        # Load the Zonos model
        self.model: "Zonos" = DEFAULT_ZONOS_MODEL

        # embed
        self.speaker_embedding: torch.Tensor = self.create_speaker_embedding()

    def create_speaker_embedding(self) -> torch.Tensor:
        if not self.audio_path.exists():
            raise FileNotFoundError(f"Voice artist audio doesn't exist or is not in this location: {self.audio_path}")

        # Load artist's voice
        wav, sampling_rate = torchaudio.load(str(self.audio_path))
        embedded = self.model.make_speaker_embedding(wav, sampling_rate) 
        torch.cuda.empty_cache()
        return embedded

    def speak(
        self,
        text: str,
        output_path: Path | str | None = None,
        **kwargs,
    ) -> tuple[torch.Tensor, int]:
        """
        Generate speech based on the text provided.
        """
        cond_dict  = make_cond_dict(
            text = text,
            speaker = self.speaker_embedding
        )

        conditioning = self.model.prepare_conditioning(cond_dict)
        codes = self.model.generate(conditioning)
        wavs = self.model.autoencoder.decode(codes).cpu()
        audio, sampling_rate = wavs[0], self.model.autoencoder.sampling_rate

        if output_path is not None:
            output_path = Path(output_path)
            torchaudio.save(str(output_path), audio, sampling_rate)
             
        return audio, sampling_rate


