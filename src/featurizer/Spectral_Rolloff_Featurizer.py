import numpy as np
"""Smapling Frame Spectral roll off featurizer

This function computes the frequency range at each sampling frame"""
def computeSpectralRolloffFrequency(stft_magnitude, frequencies, percentile):
    """Compute the spectral roll off thresholds by using percentile. For percentile calculation
    a cumulative sum method is used.
    parameters: 
        stft_magnitude: 2D ndarray containing the magnitudes of the track window's STFT 
        frequencies: frequencies at the sampling rate and window size
        percentile: float [0.001 ~ 0.499], treshold to calculate the rolloff
    returns: """

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

    # print(f"total energy: {total_energy}")
    # print(f"upper_threshold: {upper_threshold_energy}")
    # print(f"low_threshold: {lower_threshold_energy}")
    return frequencies[upper_indices], frequencies[lower_indices]
    
"""this function calls computeSpectralRolloffFrequency in order to trim each piece of the signal. We then calculate the range 
for the specific interval and average it at the end."""
def computeFrequencyRange(divided_stft_magnitudes, sampling_rate, percentile=0.05):
    """frequency range is max-min after trimming off using spectral rolloff"""
    frequencies = np.fft.rfftfreq(2048, d=1/sampling_rate)
    frequency_ranges = np.zeros((divided_stft_magnitudes.shape[0],divided_stft_magnitudes.shape[2]))
    mean_frequency_range = 0
    for i in range(divided_stft_magnitudes.shape[0]):
        upper_freq_rolloff, low_freq_rolloff = computeSpectralRolloffFrequency(divided_stft_magnitudes[i], frequencies, percentile)
        freq_range_slice = upper_freq_rolloff-low_freq_rolloff
        frequency_ranges[i] = freq_range_slice
        mean_frequency_range += np.mean(freq_range_slice)
    mean_frequency_range /= divided_stft_magnitudes.shape[0]
    return frequency_ranges, mean_frequency_range