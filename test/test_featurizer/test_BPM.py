from src.featurizer.Beats_Per_Minute_Featurizer import Tempo_Estimator
import numpy as np
from pytest import approx, fixture

DEFAULT_SAMPLE_RATE = 44100
DEFAULT_HOP_SIZE = 512
DEFAULT_WIN_SIZE = 1024
DEFAULT_GAMMA = 1000
DEFAULT_ALPHA = 1.76
DEFAULT_BPM_RANGE = (30, 300)

@fixture(scope="module")
def estimator():
    return Tempo_Estimator()

@fixture
def sample_30Hz_signal():
    impulse_signal = np.zeros(44100)
    impulse_signal[::1800] = 1
    return impulse_signal

def test_init(estimator):
    assert estimator.sr == DEFAULT_SAMPLE_RATE
    assert estimator.hop_size == DEFAULT_HOP_SIZE
    assert estimator.win_size == DEFAULT_WIN_SIZE
    assert estimator.gamma == DEFAULT_GAMMA
    assert estimator.alpha == DEFAULT_ALPHA
    assert estimator.bpm_range == DEFAULT_BPM_RANGE

def test_compute_spectrogram(estimator, sample_30Hz_signal):
    spectrogram = estimator.compute_spectrogram(sample_30Hz_signal)
    assert spectrogram is not None
    assert spectrogram.shape[0] > 0
    assert spectrogram.shape[1] > 0

def test_compute_onset_signal(estimator, sample_30Hz_signal):
    spectrogram = estimator.compute_spectrogram(sample_30Hz_signal)
    onset_signal = estimator.compute_onset_signal(spectrogram)
    assert onset_signal is not None
    assert onset_signal.shape[0] > 0
    assert np.all(onset_signal >= 0)

def test_estimate_tempo_zero_signal(estimator):
    zero_signal = np.zeros(44100)
    estimated_bpm = estimator.estimate_tempo(zero_signal)
    assert estimated_bpm > 0

def test_estimate_tempo_30Hz_impulse(estimator, sample_30Hz_signal):
    estimated_bpm = estimator.estimate_tempo(sample_30Hz_signal)
    assert estimated_bpm > 0
    assert 30 <= estimated_bpm <= 300
    assert estimated_bpm == approx(30, abs=1e-1)
