import os
import numpy as np
import librosa
import sys

# Ensure the src/ directory is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

from featurizer.main_test import Featurizer
from featurizer.Beats_Per_Minute_Featurizer import Tempo_Estimator

# Path to audio files
AUDIO_DIR = "mytest"

def extract_features(audio_file):
    """Extract features using both custom featurizer and librosa for comparison."""
    
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
    librosa_rms_db = 20 * np.log10(np.mean(librosa_rms) + 1e-6)  # Convert Librosa RMS to dB

    # Spectral Features
    librosa_centroid = np.mean(librosa.feature.spectral_centroid(y=signal_librosa, sr=sr)[0])
    librosa_rolloff = np.mean(librosa.feature.spectral_rolloff(y=signal_librosa, sr=sr)[0])
    librosa_flux = np.mean(np.sum(np.diff(np.abs(librosa.stft(signal_librosa)), axis=1).clip(min=0), axis=0))
    librosa_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=signal_librosa, sr=sr)[0])
    librosa_contrast = np.mean(librosa.feature.spectral_contrast(y=signal_librosa, sr=sr)[0])

    # Dynamic Range (Convert Librosa to dB)
    peak_amplitude = np.max(np.abs(signal_librosa))
    librosa_dynamic_range_db = 20 * np.log10(peak_amplitude + 1e-6) - librosa_rms_db  # Convert Librosa Dynamic Range to dB

    # Print Results
    print(f"\nProcessing: {os.path.basename(audio_file)}")
    print(f"**BPM**: Ours: {bpm:.2f} | Librosa: {librosa_bpm:.2f}")
    print(f"**Mean RMS (dB)**: Ours: {np.mean(collapsed_features.get('collapsed_rms', [0])):.5f} | Librosa: {librosa_rms_db:.5f}")
    print(f"**Spectral Centroid**: Ours: {np.mean(collapsed_features.get('collapsed_centroid', [0])):.2f} | Librosa: {librosa_centroid:.2f}")
    print(f"**Spectral Rolloff**: Ours: {np.mean(collapsed_features.get('collapsed_rolloff', [0])):.2f} | Librosa: {librosa_rolloff:.2f}")
    print(f"**Spectral Flux**: Ours: {np.mean(collapsed_features.get('collapsed_flux', [0])):.5f} | Librosa: {librosa_flux:.5f}")
    print(f"**Spectral Bandwidth**: Ours: {np.mean(collapsed_features.get('collapsed_bandwidth', [0])):.2f} | Librosa: {librosa_bandwidth:.2f}")
    print(f"**Spectral Contrast**: Ours: {np.mean(collapsed_features.get('collapsed_contrast', [0])):.2f} | Librosa: {librosa_contrast:.2f}")
    print(f"**Dynamic Range (dB)**: Ours: {np.mean(collapsed_features.get('collapsed_dynamic_range', [0])):.2f} | Librosa (estimated): {librosa_dynamic_range_db:.2f}")

# Process all audio files in the folder
if __name__ == "__main__":
    audio_files = [os.path.join(AUDIO_DIR, f) for f in os.listdir(AUDIO_DIR) if f.endswith(".wav")]
    
    if not audio_files:
        print("No audio files found in the directory!")
    
    for audio_file in audio_files:
        extract_features(audio_file)

