from src.featurizer.Key_and_Scale_Featurizer import Key_Estimator
from pytest import fixture
import numpy as np

DEFAULT_PROFILE_SHAPE = (12, 12)
DEFAULT_NORM = 3.4641016151377544
DEFAULT_NOTES_SHAPE = (12,)
DEFAULT_COEFFICIENTS_SHAPE = (12,)

def sample_signal(freq):
    t = np.linspace(0, 2.0, int(44100 * 2.0), endpoint=False)
    signal = np.zeros_like(t)  # Initialize a signal array with the same shape as t
    for f in freq:
        signal += 0.25 * np.sin(2 * np.pi * f * t)  # Add each sine wave to the signal
    
    return signal
    #return np.sum([0.5 * np.sin(2 * np.pi * freq * t) for f in freq], axis=0)

@fixture(scope="module")
def estimator():
    return Key_Estimator()

def test__init(estimator):
    assert estimator.major_profile.shape == DEFAULT_PROFILE_SHAPE
    assert estimator.major_profile_norm == DEFAULT_NORM
    assert estimator.minor_profile.shape == DEFAULT_PROFILE_SHAPE
    assert estimator.minor_profile_norm == DEFAULT_NORM

def test_separate_signal(estimator):
    signal = np.random.randn(44100)
    harmonic = estimator.separate_signal(signal)
    assert isinstance(harmonic, np.ndarray)
    assert harmonic.shape == signal.shape
    assert np.sum(np.abs(harmonic)) < np.sum(np.abs(signal))

def test_compute_notes(estimator):
    signal = np.random.randn(44100)
    notes = estimator.compute_notes(signal)
    assert notes.shape[0] == DEFAULT_NOTES_SHAPE[0]

def test_get_pitch_class_distribution(estimator):
    notes = np.abs(np.random.randn(12, 100))
    pcd = estimator.get_pitch_class_distribution(notes)
    assert pcd.shape == (12,)

def test_get_coefficients(estimator):
    pcd = np.random.rand(12)
    major_coeffs, minor_coeffs = estimator.get_coefficients(pcd)
    assert major_coeffs.shape == DEFAULT_COEFFICIENTS_SHAPE
    assert minor_coeffs.shape == DEFAULT_COEFFICIENTS_SHAPE

def test_estimate_keys_random_noise(estimator):
    signal = np.random.randn(44100)
    major_key, minor_key = estimator.estimate_keys(signal)
    assert isinstance(major_key, str)
    assert isinstance(minor_key, str)

def test_estimate_keys_c(estimator):
    signal = sample_signal(np.array([261.63]))
    major_key, minor_key = estimator.estimate_keys(signal)
    assert "C Major" in major_key or "C Minor" in minor_key

def test_estimate_keys_a(estimator):
    signal = sample_signal(np.array([440.00]))
    major_key, minor_key = estimator.estimate_keys(signal)
    assert "A Major" in major_key or "A Minor" in minor_key

