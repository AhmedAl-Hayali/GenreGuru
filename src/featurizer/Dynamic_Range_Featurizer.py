import numpy as np

"""divided dynamic range compute
Computes the Dynammic range in each window of the signal"""
def compute_dynamic_range(divided_signal, divided_rms):
    """
    Parameters:
        divided_signal: 3-dimensional ndarray of STFT'd signals (2-dimensional)
    returns: 
        dynamic_range: ndarray of RMS values for each window, 
        dynamic_range_mean: average value of dynamic_range
    """
    dynamic_range = np.zeros((divided_signal.shape[0], 1))
    dynamic_range_mean = 0
    for i in range(divided_signal.shape[0]):
        dynamic_max = 20 *np.log10(np.max(np.abs(divided_signal[i])))
        dynamic_range_slice = dynamic_max - divided_rms[i]
        dynamic_range[i] = dynamic_range_slice
        dynamic_range_mean += dynamic_range_slice
    dynamic_range_mean /= divided_signal.shape[0]
    return dynamic_range, dynamic_range_mean