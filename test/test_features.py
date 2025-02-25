import os
import librosa
import numpy as np
import pandas as pd
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))
from featurizer.main_featurizer import Featurizer
from featurizer.Beats_Per_Minute_Featurizer import Tempo_Estimator

# Path to the test audio file
TEST_AUDIO_FILE = "test/Serenata.wav"
OUTPUT_CSV = "test/test.csv"

def process_test_song(audio_file=TEST_AUDIO_FILE):
    """ Process a single test song and compare features with Librosa """
    print(f"Processing Test Song: {audio_file}")

    # Initialize featurizer
    feat = Featurizer()

    # Load the audio file
    signal, sr, vocal_signal, _ = feat.process_audio(audio_file, sampling_rate=44100)

    # Compute BPM
    tempo = Tempo_Estimator(sr=sr)
    bpm = tempo.estimate_tempo(signal)

    # Compute STFT and Spectral Features
    div_signal, _, _ = feat.divide_signal(signal, bpm)
    div_stft_signal, div_stft_mag = feat.divide_stft(div_signal)

    # Compute Features
    features = feat.compute_features(div_stft_mag, div_stft_mag, signal, bpm)
    compare_with_librosa(signal, sr, features)


def compare_with_librosa(signal, sr, extracted_features):
    """ Compare extracted features with Librosa's built-in functions """
    
    print("\nComparing Features with Librosa...\n")

    # Compute reference values using Librosa
    librosa_bpm = librosa.beat.tempo(y=signal, sr=sr)[0]
    librosa_rms = librosa.feature.rms(y=signal).mean()
    librosa_centroid = librosa.feature.spectral_centroid(y=signal, sr=sr).mean()
    librosa_rolloff = librosa.feature.spectral_rolloff(y=signal, sr=sr).mean()
    librosa_flux = np.sum(np.diff(np.abs(librosa.stft(signal)), axis=1).clip(min=0), axis=0).mean()
    librosa_bandwidth = librosa.feature.spectral_bandwidth(y=signal, sr=sr).mean()
    librosa_contrast = librosa.feature.spectral_contrast(y=signal, sr=sr).mean()
    librosa_dynamic_range = np.max(librosa.feature.rms(y=signal)) - np.min(librosa.feature.rms(y=signal))

    # Extracted values from our model
    our_bpm = np.mean(extracted_features["bpm"])
    our_rms = np.mean(extracted_features["collapsed_rms"])
    our_centroid = np.mean(extracted_features["collapsed_centroid"])
    our_rolloff = np.mean(extracted_features["collapsed_rolloff"])
    our_flux = np.mean(extracted_features["collapsed_flux"])
    our_bandwidth = np.mean(extracted_features["collapsed_bandwidth"])
    our_contrast = np.mean(extracted_features["collapsed_contrast"])
    our_dynamic_range = np.mean(extracted_features["collapsed_dynamic_range"])

    # Print comparison
    print("Our BPM:", our_bpm)
    print("Librosa BPM:", librosa_bpm)
    print("Our RMS:", our_rms)
    print("Librosa RMS:", librosa_rms)
    print("Our Spectral Centroid:", our_centroid)
    print("Librosa Spectral Centroid:", librosa_centroid)
    print("Our Spectral Rolloff:", our_rolloff)
    print("Librosa Spectral Rolloff:", librosa_rolloff)
    print("Our Spectral Flux:", our_flux)
    print("Librosa Spectral Flux:", librosa_flux)
    print("Our Spectral Bandwidth:", our_bandwidth)
    print("Librosa Spectral Bandwidth:", librosa_bandwidth)
    print("Our Spectral Contrast:", our_contrast)
    print("Librosa Spectral Contrast:", librosa_contrast)
    print("Our Dynamic Range:", our_dynamic_range)
    print("Librosa Dynamic Range:", librosa_dynamic_range)

    # # Check if values are within a tolerance
    # assert np.isclose(our_bpm, librosa_bpm, rtol=0.1), "BPM mismatch"
    # assert np.isclose(our_rms, librosa_rms, rtol=0.1), "RMS mismatch"
    # assert np.isclose(our_centroid, librosa_centroid, rtol=0.1), "Spectral centroid mismatch"
    # assert np.isclose(our_rolloff, librosa_rolloff, rtol=0.1), "Spectral rolloff mismatch"
    # assert np.isclose(our_flux, librosa_flux, rtol=0.1), "Spectral flux mismatch"

if __name__ == "__main__":
    process_test_song()
