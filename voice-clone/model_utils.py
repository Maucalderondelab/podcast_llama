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
        modelName: str = "Zyphra/Zonos-v0.1-transformer",
        device: torch.device = DEFAULT_DEVICE,
        **kwargs,
    ):
        audioPath = Path("tests") / VOICE_ARTISTS[voice_artist_name]
        self.device = DEFAULT_DEVICE or globals().get("device", torch.device("cpu"))

        # Load the Zonos model
        self.model = Zonos.from_pretrained(modelName, device=device)

        # embedd
        embedding_output = self._create_speaker_embedding(audioPath)
        self.wav: torch.Tensor = embedding_output[0]
        self.sr: int = embedding_output[1]
        self.speaker: zonos.model.Zonos = embedding_output[2]

    def _create_speaker_embedding(self, audioPath: Path):
        if not audioPath.exists():
            raise FileNotFoundError(f"Voice artist audio doesn't exist or is not in this location: {audioPath}")

        # Load artist's voice
        wav, sampling_rate = torchaudio.load(str(audioPath))
        return wav, sampling_rate, self.model.make_speaker_embedding(wav, sampling_rate)

