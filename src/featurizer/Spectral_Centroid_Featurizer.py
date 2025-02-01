import numpy as np

"""spectral centroid 2: computed centroid at each sampling frame"""
"""define a helper function for getSpectralCentroid"""
def computeSpectralCentroid(stft_signal_mag, frequencies):
    """Computes the spectral centroid for each sampling frame contained in the window.
    parameters:
        stft_signal_mag: 2D numpy array containing magnitude of a signal window's STFT 
        frequencies: frequencies at the sampling rate and window size
    returns:
        spec_c: spectral centroid values at each sampling frame of the signal window's STFT. """
    # compute the magnitude of the stft
    x_n = stft_signal_mag
    f_n = frequencies[:,None]
   
    # multiply each frequency bin by the magnitude
    # Centroid = (Σₙ₌₀ᴺ⁻¹ [f(n) * x(n)]) / (Σₙ₌₀ᴺ⁻¹ x(n))
    numerator = np.sum(f_n * x_n, axis = 0)
    denominator = np.sum(x_n, axis = 0)

    #if x(n)s are zero for some reason
    epsilon = 1e-6
    denominator = np.where(denominator==0, epsilon, denominator)
    
    spec_c = numerator/denominator
    # print(f"{spec_c.shape}")
    return spec_c

""" spectral centroid code adapted from @bahsoun"""
def computeSpectralCentroidsMean(divided_stft_magnitudes, sampling_rate):
    """spectral centroic calc is: Centroid = (Σₙ₌₀ᴺ⁻¹ [f(n) * x(n)]) / (Σₙ₌₀ᴺ⁻¹ x(n))
    np.fft.rfftfreq conputes f(n), need to compute spectral centroid over window in each piece of the signal
    parameters:
        divided_stft_magnitudes: 3D ndarray containing all the windows of signal's STFT magnitude values
        sampling_rate: integer, sampling rate
    returns:
        spectral_centroids: ndarray of the spectral centroid at each frame for a track window
        total_mean_spectral_centroids: float, the average of all spectral centroids over the entire track 
        mean_spectral_centroids: ndarray mean of the spectral centroid for each track window. Contains the mean of spectral_centroids"""
    frequencies = np.fft.rfftfreq(2048, d=1/sampling_rate)
    spectral_centroids = np.zeros((divided_stft_magnitudes.shape[0], computeSpectralCentroid(divided_stft_magnitudes[0], frequencies).shape[0]))
    total_mean_spectral_centroid = 0
    mean_spectral_centroids = np.zeros((divided_stft_magnitudes.shape[0],1))
    for i in range(divided_stft_magnitudes.shape[0]):
        """np.mean in order to average the spectral centroid over the window."""
        spectral_centroid_piece = computeSpectralCentroid(divided_stft_magnitudes[i], frequencies)
        spectral_centroids[i] = spectral_centroid_piece
        mean_spectral_centroid_slice = np.mean(spectral_centroid_piece)
        total_mean_spectral_centroid += mean_spectral_centroid_slice
        mean_spectral_centroids[i] = mean_spectral_centroid_slice
        
    total_mean_spectral_centroid /= divided_stft_magnitudes.shape[0]
    return spectral_centroids, total_mean_spectral_centroid, mean_spectral_centroids