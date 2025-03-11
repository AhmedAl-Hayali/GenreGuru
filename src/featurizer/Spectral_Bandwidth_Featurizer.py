import numpy as np

class SpectralBandwidth:
    """
    A class for computing spectral bandwidth and mean spectral bandwidth over multiple windows.
    """

    def __init__(self, sampling_rate=44100):
        """
        Initialize the SpectralBandwidth class.

        Parameters:
            sampling_rate (int): The sampling rate of the signal.
        """
        self.sampling_rate = sampling_rate
        self.frequencies = np.fft.rfftfreq(2048, d=1/sampling_rate)  # Precompute frequency bins

    def compute_spectral_bandwidth(self, stft_magnitude, centroid):
        """
        Computes the spectral bandwidth, which is the amplitude-weighted average of the differences 
        between the spectral components and the centroid.

        Formula: sqrt(mag[i] * (freq[i] - centroid[i])^2)
        
        Parameters:
            stft_magnitude (ndarray): 2D array of STFT magnitudes.
            centroid (ndarray): Spectral centroid values.
        
        Returns:
            bandwidth (ndarray): Computed spectral bandwidth values.
        """
        f_n = self.frequencies[:, None]  # Size adjustment
        bandwidth = np.square(f_n - centroid)
        bandwidth = stft_magnitude * bandwidth
        bandwidth = np.sqrt(bandwidth)
        return bandwidth

    def compute_spectral_bandwidth_mean(self, divided_stft_magnitudes, spectral_centroids):
        """
        Computes the mean spectral bandwidth over all windows of a signal.
        
        Parameters:
            divided_stft_magnitudes (ndarray): 3D ndarray of STFT magnitudes.
            spectral_centroids (ndarray): Spectral centroid values.
        
        Returns:
            spectral_bandwidths (ndarray): Spectral bandwidth at each frame.
            total_mean_spectral_bandwidths (float): Average spectral bandwidth over the track.
            mean_spectral_bandwidths (ndarray): Mean spectral bandwidth per window.
        """
        x, y = self.compute_spectral_bandwidth(divided_stft_magnitudes[0], spectral_centroids[0]).shape
        spectral_bandwidths = np.zeros((divided_stft_magnitudes.shape[0], x, y))
        total_mean_spectral_bandwidths = 0
        mean_spectral_bandwidths = np.zeros((divided_stft_magnitudes.shape[0], 1))

        for i in range(divided_stft_magnitudes.shape[0]):
            spectral_bandwidth_piece = self.compute_spectral_bandwidth(divided_stft_magnitudes[i], spectral_centroids[i])
            spectral_bandwidths[i] = spectral_bandwidth_piece
            mean_spectral_bandwidth_piece = np.mean(spectral_bandwidth_piece)
            total_mean_spectral_bandwidths += mean_spectral_bandwidth_piece
            mean_spectral_bandwidths[i] = mean_spectral_bandwidth_piece

        total_mean_spectral_bandwidths /= divided_stft_magnitudes.shape[0]
        return spectral_bandwidths, total_mean_spectral_bandwidths, mean_spectral_bandwidths
    