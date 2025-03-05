"""test the audio splitter module.
input:
- signal (ndarray): floating point time series representation of the signal
output:
- vocal_signal (ndarray): floating point time series representation of vocal portion
- non_vocal_signal (ndarray):floating point time series representation of instrumental portion"""

import random
import 
from featurizer.Audio_Splitter import *
AUDIO_DIR = "src/deezer_previews"
X = 1

def test_init():
    audio_files = random.sample(
    [os.path.join(AUDIO_DIR, f) for f in os.listdir(AUDIO_DIR) if f.endswith(".wav")], 
    X)

    input = audio_files[0]
    sampling_rate = 44100
    featurizer = Audio_Splitter()
    signal, sampling_rate, vocal_signal, non_vocal_signal = featurizer.process_audio(input, sampling_rate)

    assert isinstance(input, str), f"Expected str, got {type(input)}"
    assert isinstance(signal, str), f"Expected Ndarray, got {type(signal)}"
    assert isinstance(sampling_rate, str), f"Expected str, got {type(sampling_rate)}"
    assert isinstance(vocal_signal, str), f"Expected str, got {type(vocal_signal)}"
    assert isinstance(non_vocal_signal, str), f"Expected str, got {type(non_vocal_signal)}"