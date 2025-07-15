from .model_manager import TTSModel, ModelManager

from .audio.zyphra_zonos import ZonosModelLocal
from .audio.sesame_csm import ElevenLabsModelAPI
from .audio.voices import VOICE_ARTISTS

__all__ = [
    "TTSModel",
    "ModelManager",
    "ZonosModelLocal", 
    "ElevenLabsModelAPI",
    "VOICE_ARTISTS",
]
