import torch
import torchaudio

from zonos.model import Zonos
from zonos.conditioning import make_cond_dict

from dataclasses import dataclass
from pathlib import Path

__all__ = [
    "Audio",
    "Speaker",
    "SpeakerText",
    "torch_concat",
    "save_to_path",
]

# TODO
# Get device
def get_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device(torch.cuda.current_device())
    # MPS breaks for whatever reason. Uncomment when it's working.
    # if torch.mps.is_available():
    #     return torch.device("mps")
    return torch.device("cpu")

DEFAULT_DEVICE = get_device()

# Default models and speaker voice
DEFAULT_ZONOS_MODEL = Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer", device=DEFAULT_DEVICE)
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

# >>> Audio >>>
@dataclass
class Audio:
    wavtensor: torch.Tensor
    srate: int
# <<< Audio <<<

# >>> Dataclass SpeakerText >>>
@dataclass
class SpeakerText:
    speaker: "Speaker"
    text: str
# <<< Dataclass SpeakerText <<<

# >>> Speaker class >>>
class Speaker:
    def __init__(
        self,
        voice_artist_name: str,
        **kwargs,
    ):
        self.audio_path: Path = VOICE_ARTISTS[voice_artist_name]

        # Load the Zonos model
        self.model: Zonos = DEFAULT_ZONOS_MODEL

        # embed
        self.speaker_embedding: torch.Tensor = self.create_speaker_embedding()

    def create_speaker_embedding(self) -> torch.Tensor:
        if not self.audio_path.exists():
            raise FileNotFoundError(
                f"Voice artist audio doesn't exist or is not in this location: {self.audio_path}"
            )

        # Load artist's voice
        voice: Audio = Audio(*torchaudio.load(self.audio_path))
        embedded = self.model.make_speaker_embedding(voice.wavtensor, voice.srate) 
        torch.cuda.empty_cache()
        return embedded

    def speak(
        self,
        text: str,
        output_path: Path | str | None = None,
        dir_path: Path | str | None = None,
        fname: str | None = None,
        save_to_cache: bool = False,
        parents: bool = False,
        exist_ok: bool = True,
    ) -> Audio:
        """
        Generate speech based on the text provided.
        
        Args:
            text: Text to convert to speech
            output_path: Optional path to save the audio file
            **kwargs: Additional arguments
            
        Returns:
            Audio object containing the generated speech
        """
        cond_dict  = make_cond_dict(
            text = text,
            speaker = self.speaker_embedding
        )

        conditioning = self.model.prepare_conditioning(cond_dict)
        codes = self.model.generate(conditioning)
        wavs = self.model.autoencoder.decode(codes).cpu()
        voice: Audio = Audio(wavs[0], self.model.autoencoder.sampling_rate)

        if output_path is not None or dir_path is not None or fname is not None:
            save_to_path(
                voice,
                output_path, 
                dir_path, 
                fname, 
                save_to_cache, 
                parents, 
                exist_ok,
            )

        torch.cuda.empty_cache()
        return voice
# <<< Speaker class <<<

# >>> Concat Torch segments >>>
def torch_concat(
    audio_segments: list[Audio],
    output_path: Path | str | None = None,
) -> Audio:

    group_audio_segments_list = []
    for asg in audio_segments:
        group_audio_segments_list.append(asg)
    
    group_audio_segments_tuple = tuple(group_audio_segments_list)
    group_audio_segments = torch.cat(group_audio_segments_tuple, dim=1)

    sample_rate = audio_segments[0].srate

    if output_path is not None:
        torchaudio.save(Path(output_path), group_audio_segments, sample_rate)

    return Audio(group_audio_segments, sample_rate) 
# <<< Concat Torch segments <<<


# >>> save_to_path - save file to dir w/ or w/o full Path >>>
def save_to_path(
    voice: Audio,
    output_path: Path | str | None = None,
    dir_path: Path | str | None = None,
    fname: str | None = None,
    save_to_cache: bool = False,
    parents: bool = True,
    exist_ok: bool = False,
):
    assert Path(output_path).suffix not in [".mp3", ".wav"], "`output_path` must end with a valid audio file extension."
    assert Path(fname).suffix not in [".mp3", ".wav"], "`fname` must end with a valid audio file extension."

    data_path: Path = Path("..", "..", "..", "data")

    # Validate inputs are correct
    if output_path is not None:
        if dir_path is not None or fname is not None:
            warnings.warn("`output_path` provided, ignoring `dir_path` and `fname`.", UserWarning)
            full_path_file: Path = data_path / output_path

    if output_path is None:
        if dir_path is None or fname is None:
            raise ValueError("Provide either `full_path` or both `dir_path` and `fname`")
        else:
            if save_to_cache:
                full_path: Path = data_path / dir_path / "cache" 
                full_path.mkdir(parents=parents, exist_ok=exist_ok)
                full_path_file: Path = full_path / fname
            else:
                full_path: Path = data_path / dir_path
                full_path.mkdir(parents=parents, exist_ok=exist_ok)
                full_path_file: Path = full_path / fname


    torch.save(full_path_file, voice.wavtensor, voice.srate)

    _print_output = f"Audio file saved at: {full_path_file}"
    print(_print_output)
    print(len(_print_output) * "-")
# <<< save_to_path - save file to dir w/ or w/o full Path <<<
