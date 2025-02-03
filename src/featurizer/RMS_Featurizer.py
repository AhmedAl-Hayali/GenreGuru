import numpy as np

class RMSComputation:
    """
    A class for computing Root Mean Square (RMS) energy over multiple windows.
    """

    def __init__(self):
        """Initialize the RMSComputation class."""
        self.epsilon = 1e-9  # Small value to prevent log(0) errors

    """vectorized RMS computation, much faster performance and correctly caculates the values by not using mean across
    time_samples and only the localized frequency bin."""
    def compute_rms(self, divided_stft_signal_mag):
        """
        Computes the Root Mean Square (RMS) energy of an STFT magnitude signal.
        Parameters:
            divided_stft_signal_mag (3D ndarray): Magnitudes of the STFT signal.
        Returns:
            rms (ndarray): RMS values for each window.
            rms_mean (float): Average RMS value over all windows.
        """
        stft_power = np.square(divided_stft_signal_mag)

        mean_power = np.mean(stft_power, axis=-1)

        rms = np.sqrt(mean_power)

        # Decibel conversion of the RMS portionAvoid log(0) by clamping to epsilon

        rms = 20 * np.log10(np.maximum(rms, self.epsilon))
        rms_mean = np.mean(rms)
        return rms, rms_mean
