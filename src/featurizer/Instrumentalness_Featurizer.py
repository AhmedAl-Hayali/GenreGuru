import numpy as np

class InstrumentalnessComputation:
    """
    A class for computing instrumentalness of a song based on RMS values.
    """

    def __init__(self, epsilon=1e-10):
        """
        Initialize the InstrumentalnessComputation class.

        Parameters:
            epsilon (float): Small value to prevent division by zero or negative values.
        """
        self.epsilon = epsilon

    """Module for the computation of the instrumentalness of the song.
    We do so by comparing the RMS of the vocals to the original, in order to avoid 
    extra computation on the non-vocal output.
    """
    def compute_instrumentalness(self, original_rms, vocal_rms):
        """
        Computes instrumentalness [0~1] where a lower value means more vocals and a higher value means less vocals.
        Instrumentalness is being defined as:
        Instrumentalness = 1 - (vocal_energy / original_energy)

        Somewhat attempts to account for spleeter's imperfect isolation (further exacerbated by using mono input).
        Assumption: All inputs have the same shape. BPM will not be recomputed, so should have the same size.

        Parameters:
            original_rms (ndarray): Feature vector of RMS of original audio.
            vocal_rms (ndarray): Feature vector of RMS of the vocal portion.
        
        Returns:
            instrumentalness (ndarray): Instrumentalness value at each window.
            mean_instrumentalness (float): Overall instrumentalness of the entire song.
        """
        instrumentalness = np.zeros((original_rms.shape[0], 1))
        mean_instrumentalness = 0

        for i in range(original_rms.shape[0]):
            # Compute dB difference first.
            db_diff = vocal_rms[i] - original_rms[i]

            # Compute the ratio, use epsilon to avoid negative values:
            energy_ratio = 10**(db_diff / 10)
            current_instrumentalness = 1 - min(energy_ratio, 1 - self.epsilon)
            instrumentalness[i] = current_instrumentalness
            mean_instrumentalness += current_instrumentalness
        
        mean_instrumentalness /= original_rms.shape[0]
        return instrumentalness, mean_instrumentalness

    """Module for the computation of the instrumentalness of the song.
    We do so by comparing the RMS of the vocals to the original, in order to avoid 
    extra computation on the non-vocal output.
    """
    def compute_instrumentalness_vec(self, original_rms, vocal_rms):
        """
        Computes instrumentalness [0~1] where a lower value means more vocals and a higher value means less vocals.
        Instrumentalness is being defined as:
        Instrumentalness = 1 - (vocal_energy / original_energy)

        Somewhat attempts to account for spleeter's imperfect isolation (further exacerbated by using mono input).
        Assumption: All inputs have the same shape. BPM will not be recomputed, so should have the same size.

        Parameters:
            original_rms (ndarray): Feature vector of RMS of original audio.
            vocal_rms (ndarray): Feature vector of RMS of the vocal portion.
        
        Returns:
            instrumentalness (ndarray): Instrumentalness value at each window.
            mean_instrumentalness (float): Overall instrumentalness of the entire song.
        """
        db_diff = vocal_rms - original_rms
        energy_ratio = 10**(db_diff / 10)
        instrumentalness = 1 - np.minimum(energy_ratio, 1 - self.epsilon)
        # instrumentalness = 1-energy_ratio
        mean_instrumentalness = np.mean(instrumentalness)

        return instrumentalness, mean_instrumentalness
