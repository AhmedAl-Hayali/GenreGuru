import numpy as np

def computeSubbandPeak(sub_band_magnitudes, alpha=0.02):
    """Compute the subband peak"""
    # sort subband in descending order
    sorted_magnitudes = np.sort(sub_band_magnitudes, axis=0)[::-1]
    # find how many bins we need for this subband (how many peak values)
    alpha_count = max(1, int(alpha * sub_band_magnitudes.shape[0]))
    # take the average of those bins
    peak = np.mean(sorted_magnitudes[:alpha_count, :], axis=0)
    # Convert to dB scale
    return 20 * np.log10(peak + 1e-6)

def computeSubbandValley(sub_band_magnitudes, alpha=0.02):
    """Compute the subband valley"""
    # sort subband in ascending  order
    sorted_magnitudes = np.sort(sub_band_magnitudes, axis=0)
    # find how many bins we need for this subband (how many valley values)
    alpha_count = max(1, int(alpha * sub_band_magnitudes.shape[0]))
    # take the average of those bins
    valley = np.mean(sorted_magnitudes[:alpha_count, :], axis=0)
    # Convert to dB scale
    return 20 * np.log10(valley + 1e-6)

def computeSpectralContrast(sub_band):
    """Calculate contrast subband (peak - valley)"""
    peak_db = computeSubbandPeak(sub_band)
    valley_db = computeSubbandValley(sub_band)
    return peak_db - valley_db

"""This is where we will compute the mean spectral flux"""
def computeSpectralContrastMean(divided_stft_magnitudes, n_bands=7):
    num_windows, num_bins, num_frames = divided_stft_magnitudes.shape
    # Divide frequency bins into equal parts (n_bands) allows us to have the start and end indicie for each band
    bin_ranges = np.linspace(0, num_bins, num=n_bands + 1, dtype=int)

    spectral_contrast = np.zeros((num_windows, n_bands, num_frames))
    mean_spectral_contrast = np.zeros((num_windows, n_bands))

    for i in range(num_windows):
        for band_idx in range(n_bands):
            # Get the start and end indices for the subband in this window
            start_bin, end_bin = bin_ranges[band_idx], bin_ranges[band_idx + 1]

            # subband for the current window
            sub_band = divided_stft_magnitudes[i, start_bin:end_bin, :]
            if sub_band.shape[0] == 0:
                continue

            contrast = computeSpectralContrast(sub_band)
            spectral_contrast[i, band_idx, :] = contrast
            mean_spectral_contrast[i, band_idx] = np.mean(contrast)

    total_mean_spectral_contrast = np.mean(mean_spectral_contrast)
    return spectral_contrast, total_mean_spectral_contrast, mean_spectral_contrast
