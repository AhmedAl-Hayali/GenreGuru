import numpy as np

class RMSComputation:
    """
    A class for computing Root Mean Square (RMS) energy over multiple windows.
    """

    def __init__(self):
        """Initialize the RMSComputation class."""
        self.epsilon = 1e-10  # Small value to prevent log(0) errors

    """RMS compute, operates over divided signal
    computes RMS over each window, returns vector of RMS values and average RMS"""
    def compute_rms(self, divided_stft_signal_mag):
        """
        Computes the Root Mean Square (RMS) energy of an STFT magnitude signal.

        Parameters:
            divided_stft_signal_mag (3D ndarray): Magnitudes of the STFT signal.
        
        Returns:
            rms (ndarray): RMS values for each window.
            rms_mean (float): Average RMS value over all windows.
        """
        rms = np.zeros((divided_stft_signal_mag.shape[0], 1))
        rms_mean = 0

        for i in range(divided_stft_signal_mag.shape[0]):
            # Square the STFT magnitude values
            squared_signal = np.square(divided_stft_signal_mag[i])
            mean_squared = np.mean(squared_signal)
            root_mean_squared = np.sqrt(mean_squared)

            "Decibel conversion of the RMS portion"
            # Avoid log(0) by clamping to epsilon
            root_mean_squared_db = 20 * np.log10(np.maximum(root_mean_squared, self.epsilon))

            rms_mean += root_mean_squared_db
            rms[i] = root_mean_squared_db
        
        rms_mean /= divided_stft_signal_mag.shape[0]
        return rms, rms_mean
