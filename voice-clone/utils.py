import torch
from zonos.model import Zonos
from zonos.conditioning import make_cond_dict
from zonos.utils import DEFAULT_DEVICE
from model_utils import DEFAULT_ZONOS_MODEL

from pathlib import Path

# give path to directory and load *.txt story file
def load_txt(path: Path | str, fname: str | None) -> str:
    if fname is None:
        fname = str(path) + ".txt"
    dirPath = Path("tests") / path
    txtPath = Path(dirPath) / fname
    if not Path(txtPath).is_file():
        raise FileNotFoundError(f"File {txtPath} doesn't exist or is not in this location: {dirPath}")
    return txtPath.read_text()


    # audio_dict: dict[Any, str],
def generate_track(
    script: str,
    path: Path | str,
    fname= str | None,
    model: Any = DEFAULT_ZONOS_MODEL,
    save: bool = False,
    **kwargs,
) -> Any: 



    dirPath = os.path.join("tests", path)
    if audio_dict is None:
        audio_dict = load_txt(path, fname=None)

    # torch.cuda.empty_cache()

    cond_dict = make_cond_dict(text=audio_dict[ix],
                               speaker=speaker,
                               language="en-us",
                               #                       Happiness, Sadness, Disgust, Fear, Surprise, Anger, Other, Neutral
                               # emotion: list[float] = [0.3077, 0.0256, 0.0256, 0.0256, 0.0256, 0.0256, 0.2564, 0.3077],
                               emotion = [0.0377, 0.0256, 0.2056, 0.0256, 0.1256, 0.2056, 0.2564, 0.3077],
                               )
    conditioning = model.prepare_conditioning(cond_dict)
    codes = model.generate(conditioning)
    wavs = model.autoencoder.decode(codes).cpu()
    fPath = os.path.join(dirPath, txt+f"-Chunk{ix:0>2}.wav")
    if save==True:
        torchaudio.save(fPath, wavs[0], model.autoencoder.sampling_rate)
        print("Audio saved!")

    print("--------------------------------------------------")
    print(f"Generated audio chunk: {fPath}")

    return (wavs[0], model.autoencoder.sampling_rate)


# generate narration of a specific text line 
def generate_track(path, ix, fname=None, model=model_ith, audio_dict, save=False):
    dirPath = os.path.join("tests", path)
    if audio_dict is None:
        audio_dict = load_txt(path, fname=None)

    # torch.cuda.empty_cache()

    cond_dict = make_cond_dict(text=audio_dict[ix],
                               speaker=speaker,
                               language="en-us",
                               #                       Happiness, Sadness, Disgust, Fear, Surprise, Anger, Other, Neutral
                               # emotion: list[float] = [0.3077, 0.0256, 0.0256, 0.0256, 0.0256, 0.0256, 0.2564, 0.3077],
                               emotion = [0.0377, 0.0256, 0.2056, 0.0256, 0.1256, 0.2056, 0.2564, 0.3077],
                               )
    conditioning = model.prepare_conditioning(cond_dict)
    codes = model.generate(conditioning)
    wavs = model.autoencoder.decode(codes).cpu()
    fPath = os.path.join(dirPath, txt+f"-Chunk{ix:0>2}.wav")
    if save==True:
        torchaudio.save(fPath, wavs[0], model.autoencoder.sampling_rate)
        print("Audio saved!")

    print("--------------------------------------------------")
    print(f"Generated audio chunk: {fPath}")

    return (wavs[0], model.autoencoder.sampling_rate)

def torchConcat(path, concat, save=False):
    dirPath = os.path.join("tests", path)
    outfile = os.path.join(dirPath, path+"-TorchStory.wav")

    whole_track_lst = []
    for i in range(len(concat)):
        whole_track_lst.append(concat[i][0])

    whole_track_tup = tuple(whole_track_lst)
    whole_track = torch.cat(whole_track_tup, dim=1)

    if save==True:
        torchaudio.save(outfile, whole_track, concat[0][1])
        print("--------------------------------------------------")
        print(f"DONE! Torch concatenated audio file: {outfile}")
    return (whole_track, concat[0][1])


# gen narrator in one run
def znzTrain(path, fname=None, model=model, audio_dict=None):
    dirPath = os.path.join("tests", path)
    audios = []

    if audio_dict is None:
        audio_dict = load_txt(path, fname)

    for li in range(len(lst)):
        audios.append(generate_track(path, li, model=model[i]))
    return audios
