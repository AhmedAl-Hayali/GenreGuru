"""My bad attempt at an algorithm that tries to estimate the tempo of a song
- Works better on songs that have a single tempo
- For the purposes of my environment, I have mp3 files locally and then they are converted to .wav
- pip install all the libraries, you need to manually install ffmpeg and add it to %PATH% otherwise pydub
will give you file not found errors
"""
import os
import numpy as np
import librosa
import matplotlib.pyplot as plt
from pydub import AudioSegment

def mp3_to_wav(mp3_path, wav_path):
    """Convert an MP3 file to WAV using pydub."""
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")

def generate_spectrogram(signal, window_size, hop_size):
    """
    1. Compute the Short-Time Fourier Transform using librosa
    2. Square the spectrogram to get the power spectrogram
    3. Convert to the db scale for accurate vieweing
    """
    spectrogram = np.abs(librosa.stft(signal, n_fft=window_size, hop_length=hop_size, window='hann')**2)
    return spectrogram

def compute_novelty_curve(spectrogram):
    """
    1. Compute the spectral flux (novelty curve) from the spectrogram
        - Spectral flux is just the differences in the spectrogram from one time unit to the next
        - np.maximum(0, ...) takes care of the I(t, k) function 
    """
    flux = np.zeros(spectrogram.shape[1])
    for m in range(1, spectrogram.shape[1]):
        flux[m] = np.sum(np.maximum(0, np.abs(spectrogram[:, m]) - np.abs(spectrogram[:, m - 1])))
    return flux

def compute_autocorrelation(signal):
    """
    1. Compute the autocorrelation of a signal
        - autocorrelation is the easiest method for doing dominant pulse estimation
        - if you want to map to the paper, signal[tau:] = x(t + tau)
                                           signal[N - tau:] = x(t)
    """
    N = len(signal)
    autocorr = np.zeros(N)
    for tau in range(N):
        autocorr[tau] = np.sum(signal[:N - tau] * signal[tau:])
    return autocorr

def estimate_tempo(signal, fs, window_size, hop_size):
    """
    Overall process:
    1. Generate db-scaled power spectrogram of signal
    2. Compute novelty curve of spectrogram
    3. Run novelty curve through autocorrelation function
    4. arithmetic for BPM calculation
    """
    spectrogram = generate_spectrogram(signal, window_size, hop_size)
    novelty_curve = compute_novelty_curve(spectrogram)
    autocorrelated_novelty_curve = compute_autocorrelation(novelty_curve)
    """BPM = 60 / period
    period = lag * hop_size / fs
    "lag" is the term that represents the tau values calculated by the autocorrelation function
    """
    peak_lags = np.where(autocorrelated_novelty_curve == np.max(autocorrelated_novelty_curve[1:]))[0]
    if len(peak_lags) > 0:
        lag = max(peak_lags)
        tempo = 60 / (lag * (hop_size / fs))
    else:
        tempo = None
    return tempo, spectrogram, novelty_curve, autocorrelated_novelty_curve

def find_music_tempo(wav_path, window_size=1024, hop_size=512):
    """
    1. Convert .mp3 file to .wav with pydub
    2. Convert the audio to a usable digital signal with librosa
    3. Display the estimated tempo
    4. Plot power spectrogram
    5. Plot novelty curve
    6. Plot autocorrelation
    """
    signal, fs = librosa.load(wav_path, sr=None, mono=True)
    signal = signal / np.max(np.abs(signal))
    tempo, spectrogram, novelty_curve, autocorr = estimate_tempo(signal, fs, window_size, hop_size)
    print(f"Estimated Tempo: {tempo:.2f} BPM")

    """Power spectrogram plot"""
    plt.figure(figsize=(12, 12))
    plt.subplot(3, 1, 1)
    plt.imshow(spectrogram.T, origin='lower', aspect='auto', cmap='viridis', extent=[0, len(signal)/fs, 0, fs/2])
    plt.colorbar(label='Power (dB)')
    plt.title('Power Spectrogram')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')

    """Spectral Flux (Novelty Curve) Plot"""
    plt.subplot(3, 1, 2)
    plt.plot(np.arange(len(novelty_curve)) * (hop_size / fs), novelty_curve)
    plt.title('Novelty Curve (Spectral Flux)')
    plt.xlabel('Time (s)')
    plt.ylabel('Spectral Flux')

    """Autocorrelation Plot"""
    plt.subplot(3, 1, 3)
    beat_lag_start = 30
    beat_lag_end = 240
    plt.plot(np.arange(beat_lag_start, beat_lag_end) * (hop_size / fs), autocorr[beat_lag_start:beat_lag_end])
    plt.title('Autocorrelation')
    plt.xlabel('Lag (s)')
    plt.ylabel('Autocorrelation')

    plt.tight_layout()
    plt.show()

    """Delete the temporary audio file"""
    os.remove(wav_path)


audio_file_path = "path_to_mp3_file"
if __name__ == '__main__':
    wav_path = "temp_audio.wav"
    mp3_to_wav(audio_file_path, wav_path)
    find_music_tempo(wav_path)
