import pytest
import numpy as np
from src.featurizer.Spectral_Bandwidth_Featurizer import SpectralBandwidth

DEFAULT_SAMPLE_RATE = 44100
DEFAULT_STFT_MAGNITUDE = np.random.rand(1025, 16)
DEFAULT_SPECTRAL_CENTROID = np.random.rand(1, 16) * (DEFAULT_SAMPLE_RATE / 2)
DEFAULT_STFT_MAGNITUDE_WINDOWS = np.random.rand(171, 1025, 16)
DEFAULT_SPECTRAL_CENTROIDS_WINDOWS = np.random.rand(171, 1, 16) * (DEFAULT_SAMPLE_RATE / 2)

@pytest.fixture
def spectral_bandwidth():
    return SpectralBandwidth(sampling_rate=DEFAULT_SAMPLE_RATE)

def test_init(spectral_bandwidth):
    assert spectral_bandwidth.sampling_rate == DEFAULT_SAMPLE_RATE

def test_compute_spectral_bandwidth(spectral_bandwidth):
    bandwidth = spectral_bandwidth.compute_spectral_bandwidth(DEFAULT_STFT_MAGNITUDE, DEFAULT_SPECTRAL_CENTROID)
    assert bandwidth.shape == DEFAULT_STFT_MAGNITUDE.shape

def test_compute_spectral_bandwidth_mean(spectral_bandwidth):
    spectral_bandwidths, total_mean_bw, mean_bw = spectral_bandwidth.compute_spectral_bandwidth_mean(
        DEFAULT_STFT_MAGNITUDE_WINDOWS, DEFAULT_SPECTRAL_CENTROIDS_WINDOWS
    )
    assert spectral_bandwidths.shape == DEFAULT_STFT_MAGNITUDE_WINDOWS.shape
    assert mean_bw.shape == (171,1)
    assert isinstance(total_mean_bw, float)
