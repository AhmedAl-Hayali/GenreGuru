import pytest
import numpy as np
import librosa
import os
import random
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))
from featurizer.main_test import Featurizer
from featurizer.Beats_Per_Minute_Featurizer import Tempo_Estimator

# Path to the directory containing test audio files, randomly sample X files from it for brevity
AUDIO_DIR = "src/deezer_previews"
X = 50
AUDIO_FILE_PATH = [os.path.join(AUDIO_DIR, file) for file in random.sample(os.listdir(AUDIO_DIR), X)]

FEAT = Featurizer()

import matplotlib.pyplot as plt
from collections import defaultdict
mismatch_counts = defaultdict(int)

@pytest.fixture(scope="module", params=AUDIO_FILE_PATH)
def extract_features(request):
    """Extracts features and returns them in a dictionary for comparison.
    Run extract_features **only once** per file and return results."""

    audio_file = request.param
    # Initialize Featurizer
    
    # Load & process audio
    signal, sr, _, _ = FEAT.process_audio(audio_file, sampling_rate=44100)
    signal_librosa, _ = librosa.load(audio_file, sr=44100)

    # Compute BPM
    tempo = Tempo_Estimator(sr=sr)
    bpm = tempo.estimate_tempo(signal)
    librosa_bpm = librosa.beat.tempo(y=signal_librosa, sr=sr)[0]

    # Compute STFT and features
    div_signal, _, _ = FEAT.divide_signal(signal, bpm)
    _, div_stft_mag = FEAT.divide_stft(div_signal)
    collapsed_features = FEAT.compute_features(div_stft_mag, div_stft_mag, signal, bpm)

    # RMS (Convert Librosa to dB)
    librosa_rms = librosa.feature.rms(y=signal_librosa)[0]
    librosa_rms_db = 20 * np.log10(np.mean(librosa_rms) + 1e-6)  

    # Spectral Features
    librosa_centroid = np.mean(librosa.feature.spectral_centroid(y=signal_librosa, sr=sr)[0])
    librosa_rolloff = np.mean(librosa.feature.spectral_rolloff(y=signal_librosa, sr=sr)[0])
    librosa_flux = np.mean(np.sum(np.diff(np.abs(librosa.stft(signal_librosa)), axis=1).clip(min=0), axis=0))
    librosa_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=signal_librosa, sr=sr)[0])
    librosa_contrast = np.mean(librosa.feature.spectral_contrast(y=signal_librosa, sr=sr)[0])

    # Dynamic Range (Convert Librosa to dB)
    peak_amplitude = np.max(np.abs(signal_librosa))
    librosa_dynamic_range_db = 20 * np.log10(peak_amplitude + 1e-6) - librosa_rms_db  

    # Return a dictionary of results
    results = {
        "bpm_ours": bpm, 
        "bpm_librosa": librosa_bpm,
        "rms_ours": np.mean(collapsed_features.get("collapsed_rms", [0])),
        "rms_librosa": librosa_rms_db,
        "centroid_ours": np.mean(collapsed_features.get("collapsed_centroid", [0])),
        "centroid_librosa": librosa_centroid,
        "rolloff_ours": np.mean(collapsed_features.get("collapsed_rolloff", [0])),
        "rolloff_librosa": librosa_rolloff,
        "flux_ours": np.mean(collapsed_features.get("collapsed_flux", [0])),
        "flux_librosa": librosa_flux,
        "bandwidth_ours": np.mean(collapsed_features.get("collapsed_bandwidth", [0])),
        "bandwidth_librosa": librosa_bandwidth,
        "contrast_ours": np.mean(collapsed_features.get("collapsed_contrast", [0])),
        "contrast_librosa": librosa_contrast,
        "dynamic_range_ours": np.mean(collapsed_features.get("collapsed_dynamic_range", [0])),
        "dynamic_range_librosa": librosa_dynamic_range_db
    }
    return audio_file, results

@pytest.fixture(scope="module", params=AUDIO_FILE_PATH)
def extracted_features(request):
    """Run extract_features **only once** per file and return results."""
    audio_file = request.param
    results = extract_features(audio_file)
    return audio_file, results

@pytest.mark.parametrize("feature", [
    "bpm", "rms", "centroid", "rolloff", "flux", "bandwidth", "contrast", "dynamic_range"
])
def test_feature_comparison(extract_features, feature):
    """Compare our featurizer against Librosa for all features across multiple files."""
    audio_file, results = extract_features
    # Compare our feature against Librosa’s feature
    ours = results[f"{feature}_ours"]
    librosa = results[f"{feature}_librosa"]
    try:
        #large values with proportional errors and small values with fixed errors
        assert np.isclose(
            ours, librosa, 
            rtol=0.25,  # 25% relative tolerance
            atol=1.0    # Absolute tolerance of 1.0
            ), f"Feature {feature} mismatch in {audio_file}: Ours={ours}, Librosa={librosa}"
    except AssertionError:
        mismatch_counts[feature] += 1  # Increment mismatch count
        raise  # Re-raise the assertion error to keep pytest failure tracking

def test_plot_mismatches():
    """Plot both absolute mismatch counts and percentage of mismatches per feature."""
    features = list(mismatch_counts.keys())
    mismatches = [mismatch_counts[f] for f in features]

    # Compute mismatch percentage using X (number of audio files)
    mismatch_percentages = [(m / X) * 100 for m in mismatches]

    # Create the figure and subplots
    fig, axs = plt.subplots(1, 1, figsize=(10, 10))

    # First plot: Absolute mismatch counts
    axs[0].bar(features, mismatches, color="red")
    axs[0].set_xlabel("Feature")
    axs[0].set_ylabel("Number of Mismatches")
    axs[0].set_title("Feature Mismatch Counts")
    axs[0].tick_params(axis='x', rotation=45)

    # # Second plot: Percentage of mismatches
    # axs[1].bar(features, mismatch_percentages, color="blue")
    # axs[1].set_xlabel("Feature")
    # axs[1].set_ylabel("Mismatch Percentage (%)")
    # axs[1].set_title("Feature Mismatch Percentage")
    # axs[1].tick_params(axis='x', rotation=45)

    # Adjust layout and show/save
    plt.tight_layout()
    plt.savefig("feature_mismatch_plots.png")
    plt.show()