import numpy as np

class SpectralRolloff:
    """
    A class for computing spectral roll-off frequencies and frequency range.
    """

    def __init__(self, sampling_rate=44100, percentile=0.05):
        """
        Initialize the SpectralRolloff class.

        Parameters:
            sampling_rate (int): The sampling rate of the signal.
            percentile (float): Threshold to calculate roll-off.
        """
        self.sampling_rate = sampling_rate
        self.percentile = percentile
        self.frequencies = np.fft.rfftfreq(2048, d=1/sampling_rate)  # Precompute frequency bins

    def compute_spectral_rolloff_frequency(self, stft_magnitude):
        """
        Computes the spectral roll-off frequencies at each sampling frame.

        Parameters:
            stft_magnitude (ndarray): 2D ndarray containing the magnitudes of the track window's STFT.

        Returns:
            upper_rolloff (ndarray): Upper spectral roll-off frequencies.
            lower_rolloff (ndarray): Lower spectral roll-off frequencies.
        """

        # set thresholds. Two-sided percentile needed
        # eg percentile = 0.05 -> 1-0.05 = 0.95 >= 0.0
        percentile = self.percentile
        
        if (1 - percentile >= percentile): 
            lower = percentile
            upper = 1 - percentile
        else:
            lower = 1 - percentile
            upper = percentile
        
        total_energy = np.sum(stft_magnitude, axis=0)
        upper_threshold_energy = total_energy * upper
        lower_threshold_energy = total_energy * lower

        #calculate the cumulative energy along frequency bins
        cumulative_energy = np.cumsum(stft_magnitude, axis=0)

        #find freq bin where cumulative energy >= upper threshold, <= low threshold
        upper_bin = cumulative_energy >= upper_threshold_energy
        lower_bin = cumulative_energy <= lower_threshold_energy

        #argmax, argmin to get the first bins where the cum energy is < upper threshold, and then > lower threshold
        upper_indices = np.argmax(upper_bin, axis=0)
        lower_indices = np.argmin(lower_bin, axis=0)

        #check if any of the bins are 
        upper_threshold_check = np.any(upper_indices, axis=0)
        lower_threshold_check = np.any(lower_indices, axis=0)
        # handle cases where threshold is not met, we use lowest and highest freqs
        # compute time frames where no frequency bins cross our lower/upper thresholds
        upper_indices = np.where(upper_threshold_check, upper_indices, len(self.frequencies) - 1)
        lower_indices = np.where(lower_threshold_check, lower_indices, 0)

        return self.frequencies[upper_indices], self.frequencies[lower_indices]

    def compute_frequency_range(self, divided_stft_magnitudes):
        """
        Computes the frequency range after trimming off using spectral roll-off.

        Parameters:
            divided_stft_magnitudes (ndarray): 3D ndarray of STFT magnitude values.

        Returns:
            frequency_ranges (ndarray): Frequency range at each window.
            mean_frequency_range (float): Average frequency range across all windows.
        """
        num_windows = divided_stft_magnitudes.shape[0]
        frequency_ranges = np.zeros((num_windows, divided_stft_magnitudes.shape[2]))
        mean_frequency_range = 0
        for i in range(num_windows):
            upper_freq_rolloff, low_freq_rolloff = self.compute_spectral_rolloff_frequency(divided_stft_magnitudes[i])
            freq_range_slice = upper_freq_rolloff - low_freq_rolloff
            frequency_ranges[i] = freq_range_slice
            mean_frequency_range += np.mean(freq_range_slice)
        mean_frequency_range /= num_windows
        return frequency_ranges, mean_frequency_range
