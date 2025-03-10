import pytest
import numpy as np
from src.featurizer.Spectral_Centroid_Featurizer import SpectralCentroid

DEFAULT_SAMPLE_RATE = 44100
DEFAULT_STFT_MAGNITUDE = np.random.rand(1025, 16)
DEFAULT_STFT_MAGNITUDE_WINDOWS = np.random.rand(171, 1025, 16)

@pytest.fixture
def spectral_centroid():
    return SpectralCentroid(sampling_rate=DEFAULT_SAMPLE_RATE)

def test_init(spectral_centroid):
    assert spectral_centroid.sampling_rate == DEFAULT_SAMPLE_RATE

def test_compute_spectral_centroid(spectral_centroid):
    centroid = spectral_centroid.compute_spectral_centroid(DEFAULT_STFT_MAGNITUDE)
    assert centroid.shape == (16,)

def test_compute_spectral_centroids_mean(spectral_centroid):
    centroids, total_mean, mean_centroids = spectral_centroid.compute_spectral_centroids_mean(DEFAULT_STFT_MAGNITUDE_WINDOWS)
    assert centroids.shape == (171, 16)
    assert mean_centroids.shape == (171, 1)
    assert isinstance(total_mean, float)
