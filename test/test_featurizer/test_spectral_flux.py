import pytest
import numpy as np
from src.featurizer.Spectral_Flux_Featurizer import SpectralFlux

DEFAULT_STFT_MAGNITUDE = np.random.rand(1025, 16)
DEFAULT_STFT_MAGNITUDE_WINDOWS = np.random.rand(171, 1025, 16)

@pytest.fixture
def spectral_flux():
    return SpectralFlux()

def test_compute_spectral_flux(spectral_flux):
    flux = spectral_flux.compute_spectral_flux(DEFAULT_STFT_MAGNITUDE)
    assert flux.shape == (16,)

def test_compute_spectral_flux_mean(spectral_flux):
    flux, mean_flux = spectral_flux.compute_spectral_flux_mean(DEFAULT_STFT_MAGNITUDE_WINDOWS)
    assert flux.shape == (171, 16)
    assert mean_flux.shape == (171,1)
