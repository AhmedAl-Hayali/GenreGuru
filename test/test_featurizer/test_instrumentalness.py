"""
Computes instrumentalness [0~1] where a lower value means more vocals and a higher value means less vocals.
Instrumentalness is being defined as:
Instrumentalness = 1 - (vocal_energy / original_energy)
Somewhat attempts to account for spleeter's imperfect isolation (further exacerbated by using mono input).
Assumption: All inputs have the same shape. BPM will not be recomputed, so should have the same size.

tests for instrumentalness:
Parameters:
    original_rms (ndarray): Audio time series of original signal
    - check for numpy array of floats
    - check for valid RMS values range
    vocal_rms (ndarray): audio time series of isolated vocals
    - check for numpy array of floats
    - check for valid RMS values range
    - check that vocal_RMS and original_RMS have the same shape
Returns:
    instrumentalness (ndarray): Instrumentalness value at each window.
    - check for numpy array of floats
    - check for valid values range
    mean_instrumentalness (float): Overall instrumentalness of the entire song.
    - check for float type
    - check for vocal_rms, original_rms and instrumentalness to have same shape

"""
import pytest
import numpy as np
from src.featurizer.Instrumentalness_Featurizer import InstrumentalnessComputation

WINDOWS = 100
FREQUENCY_BINS = 1025

# Generate RMS values and normalize to ensure peak at 1 amplitude (0 dB), avoid log(0) with epsilon
ORIGINAL_RMS = np.abs(np.random.randn(WINDOWS, FREQUENCY_BINS)) + 1e-12
ORIGINAL_RMS /= ORIGINAL_RMS.max()  # Normalize to peak at 1
ORIGINAL_RMS = 20 * np.log10(ORIGINAL_RMS)  # Convert to dB

VOCAL_RMS = np.abs(np.random.randn(WINDOWS, FREQUENCY_BINS)) + 1e-12
VOCAL_RMS /= VOCAL_RMS.max()
VOCAL_RMS = 20 * np.log10(VOCAL_RMS)

@pytest.fixture
def Compute_Instrumentalness():
    return InstrumentalnessComputation()

def test_init(Compute_Instrumentalness):
    assert Compute_Instrumentalness

def compute_instrumentalness(Compute_Instrumentalness):
    return Compute_Instrumentalness.compute_instrumentalness()

def test_instrumentalness(Compute_Instrumentalness):
    """test Original_RMS input"""
    #test that Original RMS is ndarray of floats:
    assert isinstance(ORIGINAL_RMS, np.ndarray) and np.issubdtype(ORIGINAL_RMS.dtype, np.floating), (
        f"Expected numpy array of floats, got {type(ORIGINAL_RMS)} with dtype "
        f"{getattr(ORIGINAL_RMS, 'dtype', 'N/A')}")  #print type if not array
    
    #check for valid range. as this is decibes of a normalized signal we know that all values must be <= 0.
    assert np.issubdtype(ORIGINAL_RMS.dtype, np.floating) and np.all(ORIGINAL_RMS <= 0), (
        f"ORIGINAL_RMS must contain decibel values <= 0, "
        f"got dtype={ORIGINAL_RMS.dtype} with max={np.max(ORIGINAL_RMS):.2f}")
    
    """test Vocal_RMS input"""
    #test that Original RMS is ndarray of floats:
    assert isinstance(VOCAL_RMS, np.ndarray) and np.issubdtype(VOCAL_RMS.dtype, np.floating), (
        f"Expected numpy array of floats, got {type(VOCAL_RMS)} with dtype "
        f"{getattr(VOCAL_RMS, 'dtype', 'N/A')}")  #print type if not array
    
    #check for valid range. as this is decibes of a normalized signal we know that all values must be <= 0.
    assert np.issubdtype(VOCAL_RMS.dtype, np.floating) and np.all(VOCAL_RMS <= 0), (
        f"VOCAL_RMS must contain decibel values <= 0, "
        f"got dtype={VOCAL_RMS.dtype} with max={np.max(VOCAL_RMS):.2f}")
    
    """check they both have the same shape"""
    assert ORIGINAL_RMS.shape == VOCAL_RMS.shape, (
        f"Shape mismatch: ORIGINAL_RMS {ORIGINAL_RMS.shape} vs VOCAL_RMS {VOCAL_RMS.shape}")
    
    instrumentalness, instrumentalness_mean = Compute_Instrumentalness.compute_instrumentalness(ORIGINAL_RMS, VOCAL_RMS)

    """Instrumentalness feature check"""
    #first check that it is numpy array of floats
    assert isinstance(instrumentalness, np.ndarray) and np.issubdtype(instrumentalness.dtype, np.floating), (
        f"Expected numpy array of floats, got {type(instrumentalness)} with dtype "
        f"{getattr(instrumentalness, 'dtype', 'N/A')}")  #print type if not array
    
    #second we check for valid range, (0~1)
    assert np.all(instrumentalness >= 0) and np.all(instrumentalness <= 1), (
        f"instrumentalness values must be >= 0 "
        f"min={np.min(instrumentalness):.2f}")
    
    assert np.all(instrumentalness <= 1), (
        f"instrumentalness values must be <= 1"
        f"max={np.min(instrumentalness):.2f}")

    #check for shape integrity: 
    assert instrumentalness.shape[0] == ORIGINAL_RMS.shape[0], (
        f"Shape mismatch: instrumentalness {instrumentalness.shape} vs ORIGINAL_RMS {ORIGINAL_RMS.shape}")
    
    """instrumentalness_mean check"""
    #type check for float
    assert isinstance(instrumentalness_mean, float), f"Expected float, got {type(instrumentalness_mean)}"

    #check for range
    assert instrumentalness_mean >= 0, (
        f"instrumentalness_mean values must be >= 0, got {instrumentalness_mean} ")
    assert instrumentalness_mean <= 1, (
        f"instrumentalness_mean values must be <= 1, got {instrumentalness_mean} ")
