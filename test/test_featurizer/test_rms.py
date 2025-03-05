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
from featurizer.RMS_Featurizer import RMSComputation

def test_rms(divided_stft_signal_mag):

    rms_func = RMSComputation()
    rms, rms_mean = rms_func.compute_rms(divided_stft_signal_mag)
    """testing of the input? reused?"""
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
    
    """test RMS"""
    #test that RMS is ndarray of floats:
    assert isinstance(rms, np.ndarray) and np.issubdtype(rms.dtype, np.floating), (
        f"Expected numpy array of floats, got {type(rms)} with dtype "
        f"{getattr(rms, 'dtype', 'N/A')}")  #print type if not array
    
    #check for valid range. as this is decibes of a normalized signal we know that all values must be <= 0.
    assert np.issubdtype(rms.dtype, np.floating) and np.all(rms <= 0), (
        f"divided_signal must contain non-negative floats (STFT magnitudes), "
        f"got dtype={rms.dtype} with min={np.min(rms):.2f}")
    
    #check for shape, we need same number of bins as we have our divided signal
    assert rms.shape[0] == divided_stft_signal_mag.shape[0], (
        f"Shape mismatch: dynamic_range {rms.shape[0]} vs divided_rms {divided_stft_signal_mag.shape[0]}")

    """test rms_mean"""
    assert isinstance(rms_mean, float), f"Expected float, got {type(rms_mean)}"
