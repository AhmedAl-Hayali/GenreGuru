import numpy as np

def compute_spectral_rolloff_frequency(stft_magnitude, frequencies, percentile):
    """
    Computes the spectral roll-off frequencies at each sampling frame.
    
    Parameters:
        stft_magnitude (ndarray): 2D ndarray containing the magnitudes of the track window's STFT.
        frequencies (ndarray): Frequency values at the given sampling rate and window size.
        percentile (float): Threshold to calculate the roll-off, range [0.001 ~ 0.499].
    
    Returns:
        upper_rolloff (ndarray): Upper spectral roll-off frequencies.
        lower_rolloff (ndarray): Lower spectral roll-off frequencies.
    """

    # set thresholds. Two-sided percentile needed
    # eg percentile = 0.05 -> 1-0.05 = 0.95 >= 0.0
    
    if (1-percentile >= percentile): 
        lower = percentile
        upper = 1-percentile
    else:
        lower = 1-percentile
        upper = percentile
    
    total_energy = np.sum(stft_magnitude, axis=0)
    upper_threshold_energy = total_energy*upper
    lower_threshold_energy = total_energy*lower

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
    upper_indices = np.where(upper_threshold_check, upper_indices, len(frequencies) - 1)
    lower_indices = np.where(lower_threshold_check, lower_indices, 0)

    return frequencies[upper_indices], frequencies[lower_indices]
    
def compute_frequency_range(divided_stft_magnitudes, sampling_rate, percentile=0.05):
    """
    Computes the frequency range after trimming off using spectral roll-off.
    
    Parameters:
        divided_stft_magnitudes (ndarray): 3D ndarray of STFT magnitude values.
        sampling_rate (int): Sampling rate of the signal.
        percentile (float): Threshold to calculate the roll-off.
    
    Returns:
        frequency_ranges (ndarray): Frequency range at each window.
        mean_frequency_range (float): Average frequency range across all windows.
    """
    frequencies = np.fft.rfftfreq(2048, d=1/sampling_rate)
    frequency_ranges = np.zeros((divided_stft_magnitudes.shape[0],divided_stft_magnitudes.shape[2]))
    mean_frequency_range = 0
    for i in range(divided_stft_magnitudes.shape[0]):
        upper_freq_rolloff, low_freq_rolloff = compute_spectral_rolloff_frequency(divided_stft_magnitudes[i], frequencies, percentile)
        freq_range_slice = upper_freq_rolloff-low_freq_rolloff
        frequency_ranges[i] = freq_range_slice
        mean_frequency_range += np.mean(freq_range_slice)
    mean_frequency_range /= divided_stft_magnitudes.shape[0]
    return frequency_ranges, mean_frequency_range