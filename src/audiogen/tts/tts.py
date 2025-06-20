from audiogen.models import SpeakerText
from audiogen.models import Audio, Speaker, SpeakerText

from pathlib import Path

class TTS:
    def __init__(
        self,
        speaker: Speaker | None = None,
        text: str | None = None,
        script: list[SpeakerText] | None = None,
        output_path: Path | str | None = None,
        dir_path: Path | str | None = None,
        fname: str | None = None,
        save_to_cache: bool = False,
        parents: bool = True,
        exist_ok: bool = False,
    ) -> None:
        """
        Initialize TTS system.
        
        Args:
            speaker: Single speaker for monologue (used with text)
            text: Text for monologue (used with speaker)
            script: List of SpeakerText for multi-speaker dialogue
            output_path: Path to save final concatenated audio
            save_lines: Whether to save individual lines as separate files
        """
        # Validate input args combinations
        if script is None:
            if speaker is None or text is None:
                raise ValueError(
                    "When `script` is not provided then both `speaker` and `text` arguments are required."
                )
            self.audio_script: list[SpeakerText] = [SpeakerText(speaker=speaker, text=text)]
        else:
            if speaker is not None or text is not None:
                raise ValueError(
                    "When `script` is provided, do not use `speaker` nor `text` arguments."
                )
            self.audio_script: list[SpeakerText] = script
        
        # Store other parameters

    def speak_lines(
        self, 
        script: list[SpeakerText],
        output_path: Path | str | None = None,
        dir_path: Path | str | None = None,
        fname: str | None = None,
        save_to_cache: bool = False,
        parents: bool = True,
        exist_ok: bool = False,
    ) -> list[Audio]:
        """
        Produces audio according to the input script by calling `Speaker.speak(text)` for each text element in `script`.
        """
        audio_store: list[Audio] = []
        for i, speaker_text in enumerate(script):
            # Use named access instead of unpacking for clarity
            if save_to_cache:
                fname = Path(fname)
                _index_str = f"{i:04d}"
                new_fname = f"{fname.stem}_{_index_str}{fname.suffix}"
                _audio_ith = speaker_text.speaker.speak(
                    speaker_text.text,
                    output_path,
                    dir_path,
                    str(new_fname),
                    save_to_cache,
                    parents,
                    exist_ok,
                )
            audio_store.append(_audio_ith)
        return audio_store
