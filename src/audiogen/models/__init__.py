from .models import (
    TTSModel,
    ModelManager,
    ZonosModel, 
    ElevenLabsModel,
)

from .voices import VOICE_ARTISTS

__all__ = [
    "VOICE_ARTISTS",
    "TTSModel",
    "ModelManager",
    "ZonosModel", 
    "ElevenLabsModel",
]
