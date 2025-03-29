"""test the audio splitter module.
input:
    signal (ndarray): floating point time series representation of the signal
    - check for normalized signal
    - check for mono channel
    - check for data integrity? 
output:
    vocal_signal (ndarray): floating point time series representation of vocal portion
    non_vocal_signal (ndarray): floating point time series representation of instrumental portion
    - check that they have the same shape
    - check for mono-integrity
    - check for data integrity"""

import pytest
import random
import numpy as np
from src.featurizer.Audio_Splitter import Audio_Splitter

DURATION = 10
SAMPLING_RATE = 44100
ORIGINAL_SIGNAL = np.random.uniform(-1, 1, (DURATION * SAMPLING_RATE)).astype(np.float64)

@pytest.fixture
def audio_splitter():
    return Audio_Splitter()

def test_init(audio_splitter):
    assert audio_splitter

def split_audio(audio_splitter):
    return audio_splitter.split_audio(ORIGINAL_SIGNAL)

def test_audio_splitter(audio_splitter):
    vocal_signal, non_vocal_signal = audio_splitter.split_audio(ORIGINAL_SIGNAL)

    """check check that we still have numpy array of floats on all signals, before and after"""
    #test that ORIGINAL_SIGNAL is ndarray of floats:
    assert isinstance(ORIGINAL_SIGNAL, np.ndarray) and np.issubdtype(ORIGINAL_SIGNAL.dtype, np.floating), (
        f"Expected numpy array of floats, got {type(ORIGINAL_SIGNAL)} with dtype "
        f"{getattr(ORIGINAL_SIGNAL, 'dtype', 'N/A')}")  #print type if not array
    
    #test that vocal_signal is ndarray of floats:
    assert isinstance(vocal_signal, np.ndarray) and np.issubdtype(vocal_signal.dtype, np.floating), (
        f"Expected numpy array of floats, got {type(vocal_signal)} with dtype "
        f"{getattr(vocal_signal, 'dtype', 'N/A')}")  #print type if not array
    
    #test that non_vocal_signal is ndarray of floats:
    assert isinstance(non_vocal_signal, np.ndarray) and np.issubdtype(non_vocal_signal.dtype, np.floating), (
        f"Expected numpy array of floats, got {type(non_vocal_signal)} with dtype "
        f"{getattr(non_vocal_signal, 'dtype', 'N/A')}")  #print type if not array
    
    """check for shape integrity"""
    assert ORIGINAL_SIGNAL.shape == vocal_signal.shape, (
        f"Shape mismatch: ORIGINAL_SIGNAL {ORIGINAL_SIGNAL.shape} vs vocal_signal {vocal_signal.shape}")
    
    assert ORIGINAL_SIGNAL.shape == non_vocal_signal.shape, (
        f"Shape mismatch: ORIGINAL_SIGNAL {ORIGINAL_SIGNAL.shape} vs non_vocal_signal {non_vocal_signal.shape}")