import pytest
import numpy as np
from src.featurizer.Spectral_Rolloff_Featurizer import SpectralRolloff

DEFAULT_SAMPLE_RATE = 44100
DEFAULT_STFT_MAGNITUDE = np.random.rand(1025, 16)
DEFAULT_STFT_MAGNITUDE_WINDOWS = np.random.rand(171, 1025, 16)

@pytest.fixture
def spectral_rolloff():
    return SpectralRolloff(sampling_rate=DEFAULT_SAMPLE_RATE, percentile=0.05)

def test_init(spectral_rolloff):
    assert spectral_rolloff.sampling_rate == DEFAULT_SAMPLE_RATE
    assert spectral_rolloff.percentile == 0.05

def test_compute_spectral_rolloff_frequency(spectral_rolloff):
    upper, lower = spectral_rolloff.compute_spectral_rolloff_frequency(DEFAULT_STFT_MAGNITUDE)
    assert upper.shape == lower.shape == (16,)
    assert np.all(upper >= lower)

def test_compute_frequency_range(spectral_rolloff):
    freq_ranges, mean_range = spectral_rolloff.compute_frequency_range(DEFAULT_STFT_MAGNITUDE_WINDOWS)
    assert freq_ranges.shape == (171, 16)
    assert isinstance(mean_range, float)

def test_edge_cases(spectral_rolloff):
    zero_magnitude = np.zeros_like(DEFAULT_STFT_MAGNITUDE)
    upper, lower = spectral_rolloff.compute_spectral_rolloff_frequency(zero_magnitude)
    assert np.all(upper >= lower)
