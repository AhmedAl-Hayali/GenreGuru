import numpy as np

def compute_spectral_bandwidth(stft_magnitude, frequencies, centroid):
    """
    Computes the spectral bandwidth, which is the amplitude-weighted average of the differences 
    between the spectral components and the centroid.

    Formula: sqrt(mag[i]*(freq[i]-centroid[i])^2)
    
    Parameters:
        stft_magnitude (ndarray): 2D array of STFT magnitudes.
        frequencies (ndarray): Frequency values corresponding to STFT.
        centroid (ndarray): Spectral centroid values.
    
    Returns:
        bandwith (ndarray): Computed spectral bandwidth values.
    """
    f_n = frequencies[:, None] #size adjustment 
    bandwith = np.square(f_n - centroid)
    bandwith = stft_magnitude * bandwith
    bandwith = np.sqrt(bandwith)
    return bandwith
    
    
def compute_spectral_bandwidth_mean(divided_stft_magnitudes, spectral_centroids, sampling_rate):
    """
    Computes the mean spectral bandwidth over all windows of a signal.
    
    Parameters:
        divided_stft_magnitudes (ndarray): 3D ndarray of STFT magnitudes.
        spectral_centroids (ndarray): Spectral centroid values.
        sampling_rate (int): Sampling rate of the signal.
    
    Returns:
        spectral_bandwidths (ndarray): Spectral bandwidth at each frame.
        total_mean_spectral_bandwidths (float): Average spectral bandwidth over the track.
        mean_spectral_bandwidths (ndarray): Mean spectral bandwidth per window.
    """
    frequencies = np.fft.rfftfreq(2048, d=1/sampling_rate)
    x, y = compute_spectral_bandwidth(divided_stft_magnitudes[0], frequencies, spectral_centroids[0]).shape
    spectral_bandwidths = np.zeros((divided_stft_magnitudes.shape[0], x, y))
    total_mean_spectral_bandwidths = 0
    mean_spectral_bandwidths = np.zeros((divided_stft_magnitudes.shape[0],1))
    for i in range(divided_stft_magnitudes.shape[0]):
        spectral_bandwidth_piece = compute_spectral_bandwidth(divided_stft_magnitudes[i], frequencies, spectral_centroids[i])
        spectral_bandwidths[i] = spectral_bandwidth_piece
        mean_spectral_bandwidth_piece = np.mean(spectral_bandwidth_piece)
        total_mean_spectral_bandwidths += mean_spectral_bandwidth_piece
        mean_spectral_bandwidths[i] = mean_spectral_bandwidth_piece
    total_mean_spectral_bandwidths /= divided_stft_magnitudes.shape[0]
    return spectral_bandwidths, total_mean_spectral_bandwidths, mean_spectral_bandwidths

