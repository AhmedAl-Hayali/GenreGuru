import numpy as np

"""RMS compute, operates over divided signal
computes rms over each window, return vector of rms values and average rms"""
def compute_rms(divided_stft_signal_mag):
    """
    Parameters:
        divided_stft_signal_mag (3D ndarray) of the magnitudes of the STFT signal
    returns: 
        rms: ndarray of RMS values for each window, 
        rms_mean: average RMS value of rms
    """
    epsilon = 1e-10
    rms = np.zeros((divided_stft_signal_mag.shape[0], 1))
    rms_mean = 0
    for i in range(divided_stft_signal_mag.shape[0]):
        # print(divided_stft_signal[i])
        squared_signal = np.square(divided_stft_signal_mag[i])
        mean_squared = np.mean(squared_signal)
        root_mean_squared = np.sqrt(mean_squared)

        "decibel conversion of the rms portion"
        # Avoid log(0) by clamping to epsilon
        root_mean_squared_db = 20 * np.log10(np.maximum(root_mean_squared, epsilon))

        rms_mean += root_mean_squared_db
        rms[i] = root_mean_squared_db
    
    rms_mean /= divided_stft_signal_mag.shape[0]
    return rms, rms_mean