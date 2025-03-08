"""tests for the RMS featurizer.
Parameters:
    divided_stft_signal_mag (ndarray): 3D ndarray of magnitudes of the STFT signals.
    - check for numpy array
    - check for 3d
    - check that it contains magnitudes
Returns:
    rms (ndarray): RMS values for each window.
    - check for valid RMS ranges
    - check for shape (check that it matches STFT magnitude shape)
    rms_mean (float): Average RMS value over all windows.
"""
import numpy as np
import pytest
from src.featurizer.RMS_Featurizer import RMSComputation

WINDOWS = 100
FREQUENCY_BINS = 1025
TIME_FRAMES = 512

DIVIDED_STFT_MAG = np.abs(np.random.randn(WINDOWS, FREQUENCY_BINS, TIME_FRAMES))
DIVIDED_STFT_MAG /= np.max(DIVIDED_STFT_MAG)

# @pytest.fixture
# def divided_stft_mag():
#     # Generate a new array for each test, and normalize it
#     raw = np.abs(np.random.randn(WINDOWS, FREQUENCY_BINS, TIME_FRAMES))
#     return raw / np.max(raw)

@pytest.fixture
def Compute_RMS():
    return RMSComputation()

def test_init(Compute_RMS):
    assert Compute_RMS

def compute_rms(Compute_RMS):
    return Compute_RMS.compute_rms(DIVIDED_STFT_MAG)

def test_rms(Compute_RMS):
    """testing of the input? reused?"""
    """test divided signal is an ndarray """
    #check that it is an numpy array
    assert isinstance(DIVIDED_STFT_MAG, np.ndarray), (
        f"Expected numpy array of floats, got {type(DIVIDED_STFT_MAG)}"
        f"{getattr(DIVIDED_STFT_MAG, 'dtype', 'N/A')}")  #print type if not array

    #check that it is 3 dimensional:
    assert len(DIVIDED_STFT_MAG.shape) == 3, (
        f"divided_stft_signal_mag must be 3D, got {len(DIVIDED_STFT_MAG.shape)}D")

    #check that it contains magnitudes (non-negative floats for STFT magnitudes)
    assert np.issubdtype(DIVIDED_STFT_MAG.dtype, np.floating) and np.all(DIVIDED_STFT_MAG >= 0), (
        f"divided_signal must contain non-negative floats (STFT magnitudes), "
        f"got dtype={DIVIDED_STFT_MAG.dtype} with min={np.min(DIVIDED_STFT_MAG):.2f}")
    
    rms, rms_mean = Compute_RMS.compute_rms(DIVIDED_STFT_MAG)
    """test RMS""" 
    #test that RMS is ndarray of floats:
    assert isinstance(rms, np.ndarray) and np.issubdtype(rms.dtype, np.floating), (
        f"Expected numpy array of floats, got {type(rms)} with dtype "
        f"{getattr(rms, 'dtype', 'N/A')}")  #print type if not array
    
    #check for valid range. as this is decibes of a normalized signal we know that all values must be <= 0.
    assert np.issubdtype(rms.dtype, np.floating) and np.all(rms <= 0), (
        f"RMS must contain non-negative values, "
        f"got dtype={rms.dtype} with min={np.max(rms):.2f}")

    #check for shape, we need same number of bins as we have our divided signal
    assert rms.shape[0] == DIVIDED_STFT_MAG.shape[0], (
        f"Shape mismatch: dynamic_range {rms.shape[0]} vs divided_rms {DIVIDED_STFT_MAG.shape[0]}")

    """test rms_mean"""
    assert isinstance(rms_mean, float), f"Expected float, got {type(rms_mean)}"
    