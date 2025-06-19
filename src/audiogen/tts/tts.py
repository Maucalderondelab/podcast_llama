from audiogen.models import Audio, Speaker, SpeakerText
from audiogen.utils import torch_concat
from pathlib import Path

class TTS:
    def __init__(
        self,
        speaker: Speaker | None = None,
        text: str | None = None,
        script: list[SpeakerText] | None = None,
        output_path: Path | str | None = None,
        save_lines: bool | None = None,
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
            if (speaker is None) or (text is None):
                raise ValueError(
                    "When `script` is not provided then both `speaker` and `text` arguments are required."
                )
            self.audio_script: list[SpeakerText] = [SpeakerText(speaker=speaker, text=text)]
        else:
            if (speaker is not None) or (text is not None):
                raise ValueError(
                    "When `script` is provided, do not use `speaker` nor `text` arguments."
                )
            self.audio_script: list[SpeakerText] = script
        
        # Store other parameters
        self.output_path = output_path
        self.save_lines = save_lines

    def speak_lines(self, script: list[SpeakerText]) -> list[Audio]:
        """
        Produces audio according to the input script by calling Speaker.speak(text) 
        for each line in the script.
        """
        audio_store: list[Audio] = []
        for speaker_text in script:
            # Use named access instead of unpacking for clarity
            audio = speaker_text.speaker.speak(speaker_text.text)
            audio_store.append(audio)
        return audio_store
