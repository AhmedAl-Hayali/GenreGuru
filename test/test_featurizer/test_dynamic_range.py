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
import pytest
import random
import numpy as np
from src.featurizer.Dynamic_Range_Featurizer import DynamicRangeComputation
WINDOWS = 100
FREQUENCY_BINS = 1025
TIME_FRAMES = 512

DIVIDED_STFT_MAG = np.abs(np.random.randn(WINDOWS, FREQUENCY_BINS, TIME_FRAMES))
DIVIDED_RMS = 20 * np.log10(np.abs(np.random.randn(WINDOWS, FREQUENCY_BINS)) + 1e-12)

@pytest.fixture
def dynamic_range_computation():
    return DynamicRangeComputation()

def test_init(dynamic_range_computation):
    assert dynamic_range_computation

def compute_dynamic_range(dynamic_range_computation):
    return dynamic_range_computation.compute_dynamic_range(DIVIDED_STFT_MAG, DIVIDED_RMS)

def test_dynamic_range(dynamic_range_computation):
    dynamic_range, dynamic_range_mean = dynamic_range_computation.compute_dynamic_range(DIVIDED_STFT_MAG, DIVIDED_RMS)

    """test divided signal is an ndarray """
    #check that it is an numpy array
    assert isinstance(DIVIDED_STFT_MAG, np.ndarray), (
        f"DIVIDED_STFT_MAG Expected numpy array of floats, got {type(DIVIDED_STFT_MAG)}"
        f"{getattr(DIVIDED_STFT_MAG, 'dtype', 'N/A')}")  #print type if not array

    #check that it is 3 dimensional:
    assert len(DIVIDED_STFT_MAG.shape) == 3, (
        f"divided_stft_signal_mag must be 3D, got {len(DIVIDED_STFT_MAG.shape)}D")

    #check that it contains magnitudes (non-negative floats for STFT magnitudes)
    assert np.issubdtype(DIVIDED_STFT_MAG.dtype, np.floating) and np.all(DIVIDED_STFT_MAG >= 0), (
        f"DIVIDED_STFT_MAG must contain non-negative floats (STFT magnitudes), "
        f"got dtype={DIVIDED_STFT_MAG.dtype} with min={np.min(DIVIDED_STFT_MAG):.2f}")

    """test divided_rms is an numpy array of floats"""
    #first test for nupmy array of floats
    assert isinstance(DIVIDED_RMS, np.ndarray) and np.issubdtype(DIVIDED_RMS.dtype, np.floating), (
        f"Expected numpy array of floats, got {type(DIVIDED_RMS)} with dtype "
        f"{getattr(DIVIDED_RMS, 'dtype', 'N/A')}")  #print type if not array
    
    """test dynamic_range is numpy array of floats"""
    #first test for nupmy array of floats
    assert isinstance(dynamic_range, np.ndarray) and np.issubdtype(dynamic_range.dtype, np.floating), (
        f"Expected numpy array of floats, got {type(dynamic_range)} with dtype "
        f"{getattr(dynamic_range, 'dtype', 'N/A')}")  #print type if not array
    
    #test for same size as dynamic_range
    assert DIVIDED_RMS.shape == dynamic_range.shape, (
        f"Shape mismatch: dynamic_range {dynamic_range.shape} vs divided_rms {DIVIDED_RMS.shape}")

    """test for dynamic_range_mean: check it is a float"""
    assert isinstance(dynamic_range_mean, float), f"Expected float, got {type(dynamic_range_mean)}"
