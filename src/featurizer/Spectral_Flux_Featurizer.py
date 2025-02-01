import numpy as np

"""Spectral Flux Calculation
    this function is used to compute the spectral flux
    adapted from Mattews poc code
    """
def compute_spectral_flux(stft_magnitude):
    """Spectral flux is just the differences in the magnitudes from one time unit to the next """
    log_stft_magnitude = np.log(1 + 1000 * stft_magnitude)
    flux = np.zeros(log_stft_magnitude.shape[1])
    for m in range(1, log_stft_magnitude.shape[1]):
        flux[m] = np.sum(np.maximum(0, log_stft_magnitude[:, m] - log_stft_magnitude[:, m - 1]))
    return flux
    

"""This is where we will compute the mean spectral flux"""
def compute_spectral_flux_mean(divided_stft_magnitudes):
    spectral_flux = np.zeros_like((divided_stft_magnitudes.shape[0], divided_stft_magnitudes.shape[2]))
    total_mean_spectral_flux = 0
    mean_spectral_flux = np.zeros((divided_stft_magnitudes.shape[0],1))
    
    for i in range(divided_stft_magnitudes.shape[0]):
        spectral_flux_piece = compute_spectral_flux(divided_stft_magnitudes[i])
        spectral_flux[i] = spectral_flux_piece
        mean_spectral_flux_piece = np.mean(spectral_flux_piece)
        total_mean_spectral_flux += mean_spectral_flux_piece
        mean_spectral_flux[i] = mean_spectral_flux_piece
    total_mean_spectral_flux /= divided_stft_magnitudes.shape[0]
    return spectral_flux, total_mean_spectral_flux, mean_spectral_flux

