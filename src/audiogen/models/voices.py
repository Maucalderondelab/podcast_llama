from pathlib import Path

# Default models and speaker voice
# HYBRID_ZONOS_MODEL = Zonos.from_pretrained("Zyphra/Zonos-v0.1-hybrid", device=DEFAULT_DEVICE)
DEFAULT_MODEL_FILE_PATH = Path("tests") / "kratos-take-00-normCompress.mp3"

# voice artists
# data_path: Path = Path("..", "..", "..", "data")
data_path: Path = Path("../data/voices")
VOICE_ARTISTS = {
    "default": data_path / "kratos-take-00-normCompress.mp3",
    "british-01": data_path / "british-woman-monologue-01.mp3",
    "british-02": data_path / "british-woman-monologue-02.mp3",
    "meditation": data_path / "meditation-voiceover.mp3",
    "novel": data_path / "novel-story-narration.mp3",
    "sports": data_path / "SJohnsonVoiceOvers.mp3",
    "western": data_path / "western-woman-narration.mp3",
}


