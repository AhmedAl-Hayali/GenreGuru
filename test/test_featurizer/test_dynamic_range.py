"""Computes the dynamic range in each window of the signal.
Parameters:
    divided_stft_signal_mag (ndarray): 3D ndarray of magnitudes of the STFT signals.
    - check for numpy array
    - check for 3d
    - check that it contains magnitudes
    divided_rms (ndarray): RMS values for each window.
    - check that it is ndarray of floats
Returns:
    dynamic_range (ndarray): Dynamic range values for each window.
    dynamic_range_mean (float): Average dynamic range over all windows.
"""

import random
import numpy as np
from src.featurizer.Dynamic_Range_Featurizer import DynamicRangeComputation

AUDIO_DIR = "src/deezer_previews"
X = 1

def test_dynamic_range(divided_stft_signal_mag, divided_rms):
    DRcompute = DynamicRangeComputation()
    dynamic_range, dynamic_range_mean = DRcompute.compute_dynamic_range(divided_stft_signal_mag, divided_rms)

    """test divided signal is an ndarray """
    #check that it is an numpy array
    assert isinstance(divided_stft_signal_mag, np.ndarray), (
        f"Expected numpy array of floats, got {type(divided_stft_signal_mag)}"
        f"{getattr(divided_stft_signal_mag, 'dtype', 'N/A')}")  #print type if not array

    #check that it is 3 dimensional:
    assert len(divided_stft_signal_mag.shape) == 3, (
        f"divided_stft_signal_mag must be 3D, got {len(divided_stft_signal_mag.shape)}D")

    #check that it contains magnitudes (non-negative floats for STFT magnitudes)
    assert np.issubdtype(divided_stft_signal_mag.dtype, np.floating) and np.all(divided_stft_signal_mag >= 0), (
        f"divided_signal must contain non-negative floats (STFT magnitudes), "
        f"got dtype={divided_stft_signal_mag.dtype} with min={np.min(divided_stft_signal_mag):.2f}")

    """test divided_rms is an numpy array of floats"""
    #first test for nupmy array of floats
    assert isinstance(divided_rms, np.ndarray) and np.issubdtype(divided_rms.dtype, np.floating), (
        f"Expected numpy array of floats, got {type(divided_rms)} with dtype "
        f"{getattr(divided_rms, 'dtype', 'N/A')}")  #print type if not array
    
    """test dynamic_range is numpy array of floats"""
    #first test for nupmy array of floats
    assert isinstance(dynamic_range, np.ndarray) and np.issubdtype(dynamic_range.dtype, np.floating), (
        f"Expected numpy array of floats, got {type(dynamic_range)} with dtype "
        f"{getattr(dynamic_range, 'dtype', 'N/A')}")  #print type if not array
    
    #test for same size as dynamic_range
    assert divided_rms.shape == dynamic_range.shape, (
        f"Shape mismatch: dynamic_range {dynamic_range.shape} vs divided_rms {divided_rms.shape}")

    """test for dynamic_range_mean: check it is a float"""
    assert isinstance(dynamic_range_mean, float), f"Expected float, got {type(dynamic_range_mean)}"
