import numpy as np

class SpectralFlux:
    """
    A class for computing spectral flux and mean spectral flux.
    """

    def __init__(self):
        """Initialize the SpectralFlux class."""
        pass

    def compute_spectral_flux(self, stft_magnitude):
        """
        Computes the spectral flux, which is the difference in magnitudes from one time unit to the next.
        
        Parameters:
            stft_magnitude (ndarray): 2D array of STFT magnitudes.
        
        Returns:
            flux (ndarray): Spectral flux values for each time frame.
        """
        log_stft_magnitude = np.log(1 + 1000 * stft_magnitude)
        flux = np.zeros(log_stft_magnitude.shape[1])
        for m in range(1, log_stft_magnitude.shape[1]):
            flux[m] = np.sum(np.maximum(0, log_stft_magnitude[:, m] - log_stft_magnitude[:, m - 1]))
        return flux

    def compute_spectral_flux_mean(self, divided_stft_magnitudes):
        """
        Computes the mean spectral flux over all windows of a signal.
        
        Parameters:
            divided_stft_magnitudes (ndarray): 3D ndarray of STFT magnitude values.
        
        Returns:
            spectral_flux (ndarray): Spectral flux values for each window.
            total_mean_spectral_flux (float): Average spectral flux over all windows.
            mean_spectral_flux (ndarray): Mean spectral flux per window.
        """
        spectral_flux = np.zeros((divided_stft_magnitudes.shape[0], divided_stft_magnitudes.shape[2]))
        total_mean_spectral_flux = 0
        mean_spectral_flux = np.zeros((divided_stft_magnitudes.shape[0],1))
        
        for i in range(divided_stft_magnitudes.shape[0]):
            spectral_flux_piece = self.compute_spectral_flux(divided_stft_magnitudes[i])
            spectral_flux[i] = spectral_flux_piece
            mean_spectral_flux_piece = np.mean(spectral_flux_piece)
            total_mean_spectral_flux += mean_spectral_flux_piece
            mean_spectral_flux[i] = mean_spectral_flux_piece
        
        total_mean_spectral_flux /= divided_stft_magnitudes.shape[0]
        return spectral_flux, total_mean_spectral_flux, mean_spectral_flux
    