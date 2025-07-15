import torch
import torchaudio

from pathlib import Path
from dataclasses import dataclass
import warnings

__all = [
    "Audio",
    "load_txt",
    "torch_concat",
    "save_to_path",
]

@dataclass
class Audio:
    wavtensor: torch.Tensor
    srate: int

# >>> load_txt - from Path >>>
def load_txt(fpath: Path | str) -> str:
    fpath = Path(fpath) # works for both str and Path

    # txtPath = Path(dirPath) / fname
    if not fpath.is_file():
        raise FileNotFoundError(f"File '{fpath}' doesn't exist or is not in this location.")
    return fpath.read_text()
# <<< load_txt - from Path <<<

# >>> torch_concat >>>
def torch_concat(
    audio_segments: list[Audio],
    output_path: Path | str | None = None,
) -> Audio:
    tensors = [seg.wavtensor for seg in audio_segments]
    concatenated = torch.cat(tensors, dim=1)
    sample_rate = audio_segments[0].srate
    
    if output_path:
        torchaudio.save(Path(output_path), concatenated, sample_rate)
    
    return Audio(concatenated, sample_rate)
# <<< torch_concat <<<

# >>> save audio to path >>>
# NOTE: revisit this function saving handling is not optimal
def save_to_path(
    voice: Audio,
    output_path: Path | str | None = None,
    dir_path: Path | str | None = None,
    fname: str | None = None,
    save_to_cache: bool = False,
    parents: bool = True,
    exist_ok: bool = False,
):
    # FIX: the assertion logic - should check if suffix IS in the list
    if output_path is not None:
        assert Path(output_path).suffix in [".mp3", ".wav"], "`output_path` must end with a valid audio file extension."
    if fname is not None:
        assert Path(fname).suffix in [".mp3", ".wav"], "`fname` must end with a valid audio file extension."

    data_path: Path = Path("..", "..", "..", "data")

    # Validate inputs are correct
    if output_path is not None:
        if dir_path is not None or fname is not None:
            warnings.warn("`output_path` provided, ignoring `dir_path` and `fname`.", UserWarning)
        full_path_file: Path = data_path / output_path
    else:
        if dir_path is None or fname is None:
            raise ValueError("Provide either `output_path` or both `dir_path` and `fname`")
        else:
            if save_to_cache:
                full_path: Path = data_path / dir_path / "cache" 
                full_path.mkdir(parents=parents, exist_ok=exist_ok)
                full_path_file: Path = full_path / fname
            else:
                full_path: Path = data_path / dir_path
                full_path.mkdir(parents=parents, exist_ok=exist_ok)
                full_path_file: Path = full_path / fname

    # Fix the torch.save call - should be torchaudio.save
    torchaudio.save(full_path_file, voice.wavtensor, voice.srate)

    _print_output = f"Audio file saved at: {full_path_file}"
    print(_print_output)
    print(len(_print_output) * "-")
# <<< save audio to path <<<
