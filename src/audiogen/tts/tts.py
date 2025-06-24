from audiogen.tts.tts_utils import (
    Audio,
    Speaker, 
    SpeakerText,
    torch_concat,
    save_to_path,
)
from audiogen.models import ModelManager
from pathlib import Path

class TTS:
    def __init__(
        self,
        model_name: str = "zonos",
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
        Initialize TTS system with model management.
        
        Args:
            model_name: Name of the TTS model to use (e.g., "zonos", "elevenlabs")
            speaker: Single speaker for monologue (used with text)
            text: Text for monologue (used with speaker)
            script: List of SpeakerText for multi-speaker dialogue
            output_path: Path to save final concatenated audio
            **kwargs: Additional save parameters
        """
        self.model_name = model_name
        self.model_manager = ModelManager()
        
        # Store save parameters
        self.save_params = {
            "output_path": output_path,
            "dir_path": dir_path,
            "fname": fname,
            "save_to_cache": save_to_cache,
            "parents": parents,
            "exist_ok": exist_ok,
        }
        
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
    
    async def ensure_model_loaded(self) -> None:
        """Ensure the TTS model is loaded before generation"""
        await self.model_manager.load_model("tts", self.model_name)
    
    def speak_lines(
        self, 
        script: list[SpeakerText] | None = None,
        output_path: Path | str | None = None,
        dir_path: Path | str | None = None,
        fname: str | None = None,
        save_to_cache: bool = False,
        parents: bool = True,
        exist_ok: bool = False,
    ) -> list[Audio]:
        """
        Produces audio according to the input script by calling `Speaker.speak(text)` for each text element in `script`.
        
        Note: Model must be loaded first with await tts.ensure_model_loaded()
        """
        if script is None:
            script = self.audio_script
        
        # Check if model is loaded
        if not self.model_manager.get_model("tts", self.model_name).is_loaded:
            raise RuntimeError(f"Model '{self.model_name}' not loaded. Call await tts.ensure_model_loaded() first.")
        
        audio_store: list[Audio] = []
        for i, speaker_text in enumerate(script):
            if save_to_cache and fname:
                fname_path = Path(fname)
                _index_str = f"{i:04d}"
                new_fname = f"{fname_path.stem}_{_index_str}{fname_path.suffix}"
                
                _audio_ith = speaker_text.speaker.speak(
                    speaker_text.text,
                    output_path,
                    dir_path,
                    str(new_fname),
                    save_to_cache,
                    parents,
                    exist_ok,
                )
            else:
                _audio_ith = speaker_text.speaker.speak(speaker_text.text)
                
            audio_store.append(_audio_ith)
        
        return audio_store
    
    async def generate_audio(
        self,
        script: list[SpeakerText] | None = None,
        concatenate: bool = True,
        save_individual: bool = False,
    ) -> Audio | list[Audio]:
        """
        High-level method to generate audio with automatic model loading
        
        Args:
            script: Override the default script
            concatenate: Whether to concatenate all audio segments
            save_individual: Whether to save individual audio segments
            
        Returns:
            Single Audio object if concatenate=True, list of Audio objects otherwise
        """
        # Ensure model is loaded
        await self.ensure_model_loaded()
        
        # Generate individual audio segments
        if save_individual:
            audio_segments = self.speak_lines(script, **self.save_params)
        else:
            audio_segments = self.speak_lines(script)
        
        if concatenate:
            # Concatenate all segments
            final_audio = torch_concat(audio_segments, self.save_params.get("output_path"))
            return final_audio
        else:
            return audio_segments
    
    def get_model_status(self) -> dict:
        """Get status of the current model"""
        try:
            model = self.model_manager.get_model("tts", self.model_name)
            return {
                "model_name": self.model_name,
                "loaded": model.is_loaded,
                "type": type(model).__name__
            }
        except ValueError:
            return {
                "model_name": self.model_name,
                "loaded": False,
                "error": "Model not registered"
            }
