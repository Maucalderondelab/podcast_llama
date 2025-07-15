# from .tts_service import (
#     TTSservice,
# )

from .tts import (
    Speaker, 
    SpeakerText,
)

from .tts_utils import (
    Audio,
    load_txt,
    torch_concat,
    save_to_path,
)

__all__ = [
    # "TTSservice",
    "Speaker",
    "SpeakerText",
    "Audio",
    "load_txt",
    "torch_concat",
    "save_to_path",
]
