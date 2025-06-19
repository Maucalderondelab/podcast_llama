from audiogen.models import Audio, Speaker, SpeakerText
from pathlib import Path

class TTS:
    def __init__(
        self,
        speaker: Speaker | None = None,
        text: str | None = None,
        script: list[SpeakerText] | None = None,
        output_path: Path | str | None = None,
        save_lines: bool | None = None,
    ) -> None:  # __init__ should return None, not list[Audio]
        # If no script is provided then create one monologue
        if script is None:
            assert (speaker is not None) and (text is not None), "When `script` is not provided then arguments `speaker` and `text` are mandatory."
            # Create SpeakerText properly, not a tuple
            self.audio_script: list[SpeakerText] = [SpeakerText(speaker, text)]
        else:
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
