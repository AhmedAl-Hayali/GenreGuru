import numpy as np

"""RMS compute, operates over divided signal
computes rms over each window, return vector of rms values and average rms"""
def compute_rms(divided_signal):
    """
    Parameters:
        divided_signal: 3-dimensional ndarray of STFT'd signals (2-dimensional)
    returns: 
        rms: ndarray of RMS values for each window, 
        rms_mean: average RMS value of rms
    """
    rms = np.zeros((divided_signal.shape[0], 1))
    rms_mean = 0
    for i in range(divided_signal.shape[0]):
        squared_signal = np.square(divided_signal[i])
        mean_squared = np.mean(squared_signal)
        root_mean_squared = np.sqrt(mean_squared)
        "decibel conversion of the rms portion"
        root_mean_squared = 20*np.log10(root_mean_squared)
        rms_mean += root_mean_squared
        rms[i] = root_mean_squared
    """variance calculation""" 
    rms_mean /= divided_signal.shape[0]
    return rms, rms_mean