import pytest
import numpy as np
from src.featurizer.Spectral_Contrast_Featurizer import SpectralContrast

DEFAULT_STFT_MAGNITUDE_WINDOWS = np.random.rand(171, 1025, 16)

@pytest.fixture
def spectral_contrast():
    return SpectralContrast(n_bands=7, alpha=0.02)

def test_init(spectral_contrast):
    assert spectral_contrast.n_bands == 7
    assert spectral_contrast.alpha == 0.02

def test_compute_spectral_contrast_mean(spectral_contrast):
    contrast, total_mean, mean_contrast = spectral_contrast.compute_spectral_contrast_mean(DEFAULT_STFT_MAGNITUDE_WINDOWS)
    assert contrast.shape == (171, 7, 16)
    assert mean_contrast.shape == (171, 7)
    assert isinstance(total_mean, float)
