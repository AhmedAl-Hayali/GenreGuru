import numpy as np

class DynamicRangeComputation:
    """
    A class for computing the dynamic range of a signal over multiple windows.
    """

    def __init__(self):
        """Initialize the DynamicRangeComputation class."""
        pass  # No instance variables needed

    """Divided dynamic range compute
    Computes the dynamic range in each window of the signal.
    """
    def compute_dynamic_range(self, divided_signal, divided_rms):
        """
        Computes the dynamic range in each window of the signal.

        Parameters:
            divided_signal (ndarray): 3D ndarray of STFT'd signals.
            divided_rms (ndarray): RMS values for each window.
        
        Returns:
            dynamic_range (ndarray): Dynamic range values for each window.
            dynamic_range_mean (float): Average dynamic range over all windows.
        """
        dynamic_range = np.zeros((divided_signal.shape[0], 1))
        dynamic_range_mean = 0

        for i in range(divided_signal.shape[0]):
            dynamic_max = 20 * np.log10(np.max(np.abs(divided_signal[i])))
            dynamic_range_slice = dynamic_max - divided_rms[i]
            dynamic_range[i] = dynamic_range_slice
            dynamic_range_mean += dynamic_range_slice
        
        dynamic_range_mean /= divided_signal.shape[0]
        return dynamic_range, dynamic_range_mean
