import numpy as np

class SpectralCentroid:
    """
    A class for computing spectral centroid and mean spectral centroid over multiple windows.
    """

    def __init__(self, sampling_rate):
        """
        Initialize the SpectralCentroid class.

        Parameters:
            sampling_rate (int): The sampling rate of the signal.
        """
        self.sampling_rate = sampling_rate
        self.frequencies = np.fft.rfftfreq(2048, d=1/sampling_rate)  # Precompute frequency bins

    def compute_spectral_centroid(self, stft_signal_mag):
        """Computes the spectral centroid for each sampling frame contained in the window.
        
        Parameters:
            stft_signal_mag: 2D numpy array containing magnitude of a signal window's STFT.
        
        Returns:
            spec_c: Spectral centroid values at each sampling frame of the signal window's STFT.
        """
        # compute the magnitude of the stft
        x_n = stft_signal_mag
        f_n = self.frequencies[:, None]
    
        # multiply each frequency bin by the magnitude
        # Centroid = (Σₙ₌₀ᴺ⁻¹ [f(n) * x(n)]) / (Σₙ₌₀ᴺ⁻¹ x(n))
        numerator = np.sum(f_n * x_n, axis=0)
        denominator = np.sum(x_n, axis=0)

        # If x(n) values are zero, avoid division by zero
        epsilon = 1e-6
        denominator = np.where(denominator == 0, epsilon, denominator)
        
        spec_c = numerator / denominator
        return spec_c

    """ spectral centroid code adapted from @bahsoun """
    def compute_spectral_centroids_mean(self, divided_stft_magnitudes):
        """Spectral centroid calculation: Centroid = (Σₙ₌₀ᴺ⁻¹ [f(n) * x(n)]) / (Σₙ₌₀ᴺ⁻¹ x(n))
        np.fft.rfftfreq computes f(n), need to compute spectral centroid over window in each piece of the signal.
        
        Parameters:
            divided_stft_magnitudes (ndarray): 3D ndarray containing all the windows of signal's STFT magnitude values.
        
        Returns:
            spectral_centroids (ndarray): Spectral centroid at each frame for a track window.
            total_mean_spectral_centroids (float): Average of all spectral centroids over the entire track.
            mean_spectral_centroids (ndarray): Mean spectral centroid for each track window.
        """
        spectral_centroids = np.zeros((divided_stft_magnitudes.shape[0], 
                                       self.compute_spectral_centroid(divided_stft_magnitudes[0]).shape[0]))
        total_mean_spectral_centroid = 0
        mean_spectral_centroids = np.zeros((divided_stft_magnitudes.shape[0], 1))

        for i in range(divided_stft_magnitudes.shape[0]):
            """np.mean in order to average the spectral centroid over the window."""
            spectral_centroid_piece = self.compute_spectral_centroid(divided_stft_magnitudes[i])
            spectral_centroids[i] = spectral_centroid_piece
            mean_spectral_centroid_slice = np.mean(spectral_centroid_piece)
            total_mean_spectral_centroid += mean_spectral_centroid_slice
            mean_spectral_centroids[i] = mean_spectral_centroid_slice
            
        total_mean_spectral_centroid /= divided_stft_magnitudes.shape[0]
        return spectral_centroids, total_mean_spectral_centroid, mean_spectral_centroids
