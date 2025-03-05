"""audio processor module test  of main featurizer
Parameters:
    audio_file_path (str): file path of the audio file
    sampling_rate(int): sampling rate for the algo

Returns:
    signal (ndarray): floating point time series representation of song. 
    - the size is length of the song (seconds) * sampling rate, which gives the number of frequency samples
    sampling_rate (int): value is the same as input
    vocal_signal (ndarray): floating point time series representation of vocal portion
    non_vocal_signal (ndarray):floating point time series representation of instrumental portion
"""
import pytest
import random
import wave
import numpy as np
import os
from src.featurizer.main_featurizer import Featurizer

AUDIO_DIR = "src/deezer_previews"

#grab random audio file path
AUDIO_FILE_PATH = random.sample(
    [os.path.join(AUDIO_DIR, f) for f in os.listdir(AUDIO_DIR) if f.endswith(".wav")], 
    1)[0]

SAMPLING_RATE = 44100

@pytest.fixture
def featurizer():
    return Featurizer()

def test_init(featurizer):
    assert featurizer.sampling_rate == SAMPLING_RATE

def process_audio(featurizer):
    return featurizer.process_audio(AUDIO_FILE_PATH, SAMPLING_RATE)

#compute the duration of the song in seconds in order to assertain the length of signal
def compute_expected_size(file_path, sampling_rate):
    with wave.open(file_path, 'rb') as wav_file:
        frames = wav_file.getnframes()  #Total number of audio frames
        framerate = wav_file.getframerate()  #Sample rate (frames per second)
        duration = frames / framerate
        return int(duration*sampling_rate) #typecast for typematching, return the expected size

def test_process_audio(process_audio):
    #random sampling of an audio file
    sampling_rate = 44100
    signal, sampling_rate_after, vocal_signal, non_vocal_signal = featurizer.process_audio(AUDIO_FILE_PATH, SAMPLING_RATE)
    
    #compute the length of the audio file to assert ndarray shape. Vocal and non-vocal signal share the same duration
    expected_size = compute_expected_size(input, sampling_rate)

    #for input, it is just an audio file path, so we check for string type.
    assert isinstance(AUDIO_FILE_PATH, str), f"Expected str, got {type(AUDIO_FILE_PATH)}"

    """for signal, we need to check for ndarray, contains floats, and shape. """
    #first, check for ndarray that contains floats:
    assert isinstance(signal, np.ndarray) and np.issubdtype(signal.dtype, np.floating), (
        f"Expected numpy array of floats, got {type(signal)} with dtype "
        f"{getattr(signal, 'dtype', 'N/A')}")  #print type if not array
    
    #second we check for the shape:
    assert signal.shape[0] == expected_size, (f"Expected shape {expected_size}, got {signal.shape}")

    """sampling_rate we check for type, and for no change between smapling_rate before and after."""
    assert isinstance(sampling_rate, int), f"Expected int, got {type(sampling_rate)}"
    assert sampling_rate_after == SAMPLING_RATE

    """vocal signal we check for ndarray, contains flats, and shape."""
    #first, check for ndarray that contains floats:
    assert isinstance(vocal_signal, np.ndarray) and np.issubdtype(vocal_signal.dtype, np.floating), (
        f"Expected numpy array of floats, got {type(vocal_signal)} with dtype "
        f"{getattr(vocal_signal, 'dtype', 'N/A')}")  #print type if not array
    
    #second we check for the shape:
    assert vocal_signal.shape[0] == expected_size, (f"Expected shape {expected_size}, got {vocal_signal.shape}")

    """non-vocal signal we check for ndarray, contains flats, and shape."""
    #first, check for ndarray that contains floats:
    assert isinstance(non_vocal_signal, np.ndarray) and np.issubdtype(non_vocal_signal.dtype, np.floating), (
        f"Expected numpy array of floats, got {type(non_vocal_signal)} with dtype "
        f"{getattr(non_vocal_signal, 'dtype', 'N/A')}")  #print type if not array
    
    #second we check for the shape:
    assert non_vocal_signal.shape[0] == expected_size, (f"Expected shape {expected_size}, got {non_vocal_signal.shape}")
