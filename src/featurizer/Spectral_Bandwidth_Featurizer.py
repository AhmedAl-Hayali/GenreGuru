import numpy as np

"""Spectral Bandwidth Calculation
    this function is used to compute the spectral bandwidth: it takes in the stft magnitudes, the frequences and the spectral centroid
    the bandwidth is the amplitude weighted average of the differences between the spectral components and the centroid"""
def compute_spectral_bandwidth(stft_magnitude, frequencies, centroid):
    """formula: sqrt(mag[i]*(freq[i]-centroid[i])^2)"""
    f_n = frequencies[:, None] #size adjustment 
    bandwith = np.square(f_n - centroid)
    bandwith = stft_magnitude * bandwith
    bandwith = np.sqrt(bandwith)
    # print("this is the stft magnitudes: ", stft_magnitude.shape)
    # print("this is the stft freq: ", frequencies.shape)
    # print("this is the stft centroid: ", centroid.shape)
    return bandwith
    


"""This is where we will comput the mean spectral bandwith"""
def compute_spectral_bandwidth_mean(divided_stft_magnitudes, spectral_centroids, sampling_rate):
    # spectral_centroid, _, _ = computeSpectralCentroidsMean(divided_stft_magnitudes, sampling_rate)
    frequencies = np.fft.rfftfreq(2048, d=1/sampling_rate)
    x, y = compute_spectral_bandwidth(divided_stft_magnitudes[0], frequencies, spectral_centroids[0]).shape
    spectral_bandwidths = np.zeros((divided_stft_magnitudes.shape[0], x, y))
    # spectral_bandwidths = np.zeros((divided_stft_magnitudes.shape[0], spectral_centroids.shape[0]))
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

