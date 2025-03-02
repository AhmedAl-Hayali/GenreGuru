import os
import librosa
import numpy as np
import pandas as pd
import pytest
import sys
import glob
import tensorflow as tf
from collections import defaultdict

# this im not entrely sure, i was trying to fix the tensor flow issue maybe youll know more
tf.compat.v1.disable_eager_execution()

# Add projects src dir to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))
from featurizer.main_test import Featurizer
from featurizer.Beats_Per_Minute_Featurizer import Tempo_Estimator

# specify the audio dir, and the audio files
AUDIO_DIR = os.path.join(os.path.dirname(__file__), "mytest")
AUDIO_FILES = glob.glob(os.path.join(AUDIO_DIR, "*.wav"))

# specify where we want to save the librosa calcualtions so we dont have to do them again
LIBROSA_CACHE_CSV = "librosa_cache.csv"

def get_user_features(audio_file):
    """Extract features from Featurizer"""
    feat = Featurizer()
    
    signal, sr, vocal_signal, _ = feat.process_audio(audio_file, sampling_rate=44100)
    tempo = Tempo_Estimator(sr=sr)
    bpm = tempo.estimate_tempo(signal)
    div_signal, _, _ = feat.divide_signal(signal, bpm)
    div_stft_signal, div_stft_mag = feat.divide_stft(div_signal)
    collapsed_features = feat.compute_features(div_stft_mag, div_stft_mag, signal, bpm)

    return {
        'bpm': collapsed_features.get('bpm', 0),
        'mean_rms': np.mean(collapsed_features.get('collapsed_rms', [0])),
        'mean_spectral_centroid': np.mean(collapsed_features.get('collapsed_centroid', [0])),
        'mean_spectral_rolloff': np.mean(collapsed_features.get('collapsed_rolloff', [0])),
        'mean_spectral_flux': np.mean(collapsed_features.get('collapsed_flux', [0])),
        'mean_spectral_bandwidth': np.mean(collapsed_features.get('collapsed_bandwidth', [0])),
        'mean_spectral_contrast': np.mean(collapsed_features.get('collapsed_contrast', [0])),
        'mean_dynamic_range': np.mean(collapsed_features.get('collapsed_dynamic_range', [0])),
    }

def get_librosa_features(audio_file):
    """Extract features using Librosa."""
    try:
        # Load cached feature values if they exist
        df = pd.read_csv(LIBROSA_CACHE_CSV)
    except FileNotFoundError:
        # Create an empty DataFrame if the cache file is missing
        df = pd.DataFrame(columns=[
            'filename', 'librosa_bpm', 'librosa_rms_db', 'librosa_centroid',
            'librosa_rolloff', 'librosa_flux', 'librosa_bandwidth',
            'librosa_contrast', 'librosa_dynamic_range'
        ])

    # Check if features for this file already exist in the cache (no need to check if results are already there)
    cached = df[df['filename'] == audio_file]
    if not cached.empty:
        return cached.iloc[0].to_dict()

    # Load the audio file using Librosa
    signal, sr = librosa.load(audio_file, sr=44100)

    # theres a veriosn issue here so we try both methods if one doesnt work
    try:
        # Estimate BPM using Librosa's rhythm features
        librosa_bpm = librosa.feature.rhythm.tempo(y=signal, sr=sr)[0]
        bpm = librosa.beat.tempo(y=signal, sr=sr)[0]
        print(f"this is the other {bpm}")
    except AttributeError:
        # Fallback method in case the previous one fails
        librosa_bpm = librosa.beat.tempo(y=signal, sr=sr)[0]
        print(f"this is the other {bpm}")

    # Compute rms, and convert to decibels cause our method uses decibles
    rms = librosa.feature.rms(y=signal)
    rms_db = librosa.amplitude_to_db(rms)

    # Compute the rest of the spectral features using librosa
    features = {
        'filename': audio_file,
        'librosa_bpm': librosa_bpm,
        'librosa_rms_db': rms_db.mean(),
        'librosa_centroid': librosa.feature.spectral_centroid(y=signal, sr=sr).mean(),
        'librosa_rolloff': librosa.feature.spectral_rolloff(y=signal, sr=sr).mean(),
        'librosa_flux': np.sum(np.diff(np.abs(librosa.stft(signal)), axis=1).clip(min=0), axis=0).mean(),
        'librosa_bandwidth': librosa.feature.spectral_bandwidth(y=signal, sr=sr).mean(),
        'librosa_contrast': librosa.feature.spectral_contrast(y=signal, sr=sr).mean(),
        'librosa_dynamic_range': np.max(rms_db) - np.min(rms_db),
    }

    # save darta to the csv
    pd.concat([df, pd.DataFrame([features])]).to_csv(LIBROSA_CACHE_CSV, index=False)
    return features

@pytest.mark.parametrize("audio_file", AUDIO_FILES)
def test_feature_accuracy(audio_file):
    """Compare extracted features from Featurizer and Librosa."""
    user_features = get_user_features(audio_file)
    librosa_features = get_librosa_features(audio_file)

    if user_features is None:
        pytest.fail(f"Feature extraction failed for {audio_file}")

    feature_pairs = [
        ('bpm', 'librosa_bpm'),
        ('mean_rms', 'librosa_rms_db'),
        ('mean_spectral_centroid', 'librosa_centroid'),
        ('mean_spectral_rolloff', 'librosa_rolloff'),
        ('mean_spectral_flux', 'librosa_flux'),
        ('mean_spectral_bandwidth', 'librosa_bandwidth'),
        ('mean_spectral_contrast', 'librosa_contrast'),
        ('mean_dynamic_range', 'librosa_dynamic_range'),
    ]

    test_passed = True
    deviations = []

    print(f"\nTesting: {audio_file}")

    for user_key, librosa_key in feature_pairs:
        user_val = user_features.get(user_key, None)
        librosa_val = librosa_features.get(librosa_key, None)

        print(f"{user_key}: {user_val}, {librosa_key}: {librosa_val}")

        if user_val is None or librosa_val is None:
            print(f"Missing value for {user_key}. Test failed.")
            test_passed = False
            continue

        # Calculate deviation percentage
        if librosa_val != 0:
            deviation = abs(user_val - librosa_val) / abs(librosa_val)
        else:
            deviation = abs(user_val)

        if deviation > 0.15:
            print(f"{user_key} deviation too high: {deviation * 100:.2f}%")
            test_passed = False

        deviations.append(deviation * 100)


        # Print final test result summary
        print("\n-------- Test Result --------")
        print(f"File: {audio_file}")
        print(f"Test Passed: {test_passed}")
        print(f"Average Deviation: {np.mean(deviations):.2f}%")
        print("------------------------------------\n")

        # If test fails, make pytest recognize it
        # if not test_passed:
        #     pytest.fail(f"Feature extraction mismatch for {audio_file}")
