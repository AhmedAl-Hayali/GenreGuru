import numpy as np

class DynamicRangeComputation:
    """
    A class for computing the dynamic range of a signal over multiple windows.
    """

    def __init__(self):
        """Initialize the DynamicRangeComputation class."""

        self.epsilon = 1e-10
        pass  # No instance variables needed
    
    """Divided dynamic range compute
    Computes the dynamic range at each frame for each window of the song."""
    def compute_dynamic_range(self, divided_stft_signal_mag, divided_rms):
        """
        Computes the dynamic range in each window of the signal.

        Parameters:
            divided_signal (ndarray): 3D ndarray of STFT'd signals.
            divided_rms (ndarray): RMS values for each window.
        
        Returns:
            dynamic_range (ndarray): Dynamic range values for each window.
            dynamic_range_mean (float): Average dynamic range over all windows.
        """
        # first need to compute the max decibel at each frame. 
        dynamic_max = np.max(divided_stft_signal_mag, axis = -1)
    
        # convert to db
        dynamic_max = 20 * np.log10(np.maximum(dynamic_max, self.epsilon))

        dynamic_range = dynamic_max - divided_rms
        dynamic_range_mean = np.mean(dynamic_range)
        return dynamic_range, dynamic_range_mean

