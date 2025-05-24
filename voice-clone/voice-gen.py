import numpy as np

import torch
import torchaudio
from zonos.model import Zonos
from zonos.conditioning import make_cond_dict
from zonos.utils import DEFAULT_DEVICE as device

import wave

import os

# from moviepy.editor import VideoFileClip # I just need moviepy.editor.VideoFileClip, but for versioning conflicts editor is not there anymore, I'm downgrading to v==1.0.3|
from IPython.display import Audio
import librosa
from scipy.signal import butter, filtfilt

# load sample audio
kratos_path00 = os.path.join("tests", "kratos-take-00.mp3")
krts, krts_sr = librosa.load(kratos_path00)

# Shift the pitch down by 2 semitones
pitch_shifted = librosa.effects.pitch_shift(y=krts, sr=krts_sr, n_steps=-0.3, bins_per_octave=24, scale=True)

# model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-hybrid", device="cuda")
model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer", device=device)

# Directory paths
textPath = os.path.join("tests")

# load sample voice
wav, sampling_rate = torchaudio.load(kratos_path00)
speaker = model.make_speaker_embedding(wav, sampling_rate)

def loadTxt(txt):
    dirPath = os.path.join("tests", txt)
    filePath = os.path.join("tests", txt, txt+".txt")
    if not os.path.exists(txt):
        print(f"creating directory at: {dirPath}")
        os.makedirs(txt)
    ff = []
    with open(filePath, "r") as file:
        print(f"loading file: {filePath}")
        for li in file:
           ff.append(li) 
    file.close()
    return ff

# train
cond_dict = make_cond_dict(text="Get back! I've got a bomb", speaker=speaker, language="en-us")
conditioning = model.prepare_conditioning(cond_dict)

codes = model.generate(conditioning)
wavs = model.autoencoder.decode(codes).cpu()
