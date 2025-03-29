import numpy as np

class SpectralContrast:
    """
    A class for computing spectral contrast over multiple frequency bands.
    """

    def __init__(self, n_bands=7, alpha=0.02):
        """
        Initialize the SpectralContrast class.

        Parameters:
            n_bands (int): Number of frequency bands to divide into (default is 7).
            alpha (float): Fraction of peak/valley magnitudes to average (default is 0.02).
        """
        self.n_bands = n_bands
        self.alpha = alpha

    def compute_subband_peak(self, sub_band_magnitudes):
        """
        Computes the peak value of a subband by averaging the top alpha-percent of its magnitudes.
        
        Parameters:
            sub_band_magnitudes (ndarray): 2D ndarray containing the subband magnitudes.
        
        Returns:
            peak (ndarray): Peak values in dB scale for each frame.
        """
        # sort subband in descending order
        sorted_magnitudes = np.sort(sub_band_magnitudes, axis=0)[::-1]
        # find how many bins we need for this subband (how many peak values)
        alpha_count = max(1, int(self.alpha * sub_band_magnitudes.shape[0]))
        # take the average of those bins
        peak = np.mean(sorted_magnitudes[:alpha_count, :], axis=0)
        # Convert to dB scale
        return 20 * np.log10(peak + 1e-6)

    def compute_subband_valley(self, sub_band_magnitudes):
        """
        Computes the valley value of a subband by averaging the lowest alpha-percent of its magnitudes.
        
        Parameters:
            sub_band_magnitudes (ndarray): 2D ndarray containing the subband magnitudes.
        
        Returns:
            valley (ndarray): Valley values in dB scale for each frame.
        """
        # sort subband in ascending  order
        sorted_magnitudes = np.sort(sub_band_magnitudes, axis=0)
        # find how many bins we need for this subband (how many valley values)
        alpha_count = max(1, int(self.alpha * sub_band_magnitudes.shape[0]))
        # take the average of those bins
        valley = np.mean(sorted_magnitudes[:alpha_count, :], axis=0)
        # Convert to dB scale
        return 20 * np.log10(valley + 1e-6)

    def compute_spectral_contrast(self, sub_band):
        """
        Computes the spectral contrast of a subband as the difference between peak and valley values.
        
        Parameters:
            sub_band (ndarray): 2D ndarray containing the subband magnitudes.
        
        Returns:
            spectral_contrast (ndarray): Spectral contrast values for each frame.
        """
        peak_db = self.compute_subband_peak(sub_band)
        valley_db = self.compute_subband_valley(sub_band)
        return peak_db - valley_db

    def compute_spectral_contrast_mean(self, divided_stft_magnitudes):
        """
        Computes the spectral contrast over multiple windows of a signal, dividing the frequency range into bands.
        
        Parameters:
            divided_stft_magnitudes (ndarray): 3D ndarray of STFT magnitude values.
        
        Returns:
            spectral_contrast (ndarray): Spectral contrast values for each window and band.
            total_mean_spectral_contrast (float): Average spectral contrast over all windows and bands.
            mean_spectral_contrast (ndarray): Mean spectral contrast per window and band.
        """
        num_windows, num_bins, num_frames = divided_stft_magnitudes.shape
        # Divide frequency bins into equal parts (n_bands) allows us to have the start and end indices for each band
        bin_ranges = np.linspace(0, num_bins, num=self.n_bands + 1, dtype=int)

        spectral_contrast = np.zeros((num_windows, self.n_bands, num_frames))
        mean_spectral_contrast = np.zeros((num_windows, self.n_bands))

        for i in range(num_windows):
            for band_idx in range(self.n_bands):
                # Get the start and end indices for the subband in this window
                start_bin, end_bin = bin_ranges[band_idx], bin_ranges[band_idx + 1]

                # subband for the current window
                sub_band = divided_stft_magnitudes[i, start_bin:end_bin, :]
                if sub_band.shape[0] == 0:
                    continue

                contrast = self.compute_spectral_contrast(sub_band)
                spectral_contrast[i, band_idx, :] = contrast
                mean_spectral_contrast[i, band_idx] = np.mean(contrast)

        total_mean_spectral_contrast = np.mean(mean_spectral_contrast)
        return spectral_contrast, total_mean_spectral_contrast, mean_spectral_contrast
