import os
import numpy as np
import librosa
import sys

# Ensure the src/ directory is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))
from featurizer.main_test import Featurizer
from featurizer.Beats_Per_Minute_Featurizer import Tempo_Estimator

def extract_features(audio_file):
    """Extracts features and returns them in a dictionary for comparison."""
    
    # Initialize Featurizer
    feat = Featurizer()
    
    # Load & process audio
    signal, sr, vocal_signal, _ = feat.process_audio(audio_file, sampling_rate=44100)
    signal_librosa, sr_librosa = librosa.load(audio_file, sr=44100)

    # Compute BPM
    tempo = Tempo_Estimator(sr=sr)
    bpm = tempo.estimate_tempo(signal)
    librosa_bpm = librosa.beat.tempo(y=signal_librosa, sr=sr)[0]

    # Compute STFT and features
    div_signal, _, _ = feat.divide_signal(signal, bpm)
    div_stft_signal, div_stft_mag = feat.divide_stft(div_signal)
    collapsed_features = feat.compute_features(div_stft_mag, div_stft_mag, signal, bpm)

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
    return {
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
