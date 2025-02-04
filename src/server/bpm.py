import numpy as np
import scipy.signal as signal
import librosa

class Tempo_Estimator:
    def __init__(self, audio_path, sr=22050, hop_size=512, win_size=1024, gamma=1000, alpha=1.76, bpm_range=(30, 150)):
        self.audio_path = audio_path
        self.sr = sr
        self.hop_size = hop_size
        self.win_size = win_size
        self.gamma = gamma
        self.alpha = alpha
        self.bpm_range = bpm_range
        self.y, _ = librosa.load(audio_path, sr=self.sr, mono=True)
    
    def compute_spectrogram(self):
        window = signal.windows.hamming(self.win_size, sym=False)
        spectrogram = np.abs(librosa.stft(self.y, n_fft=self.win_size, hop_length=self.hop_size, window=window))**2
        return spectrogram
    
    def compute_onset_signal(self, spectrogram):
        compressed_spectrogram = np.log1p(self.gamma * spectrogram)
        onset_signal = np.sum(np.diff(compressed_spectrogram, axis=1).clip(min=0), axis=0)
        onset_signal[onset_signal < self.alpha] = 0
        return onset_signal
    
    def estimate_tempo(self):
        spectrogram = self.compute_spectrogram()
        onset_signal = self.compute_onset_signal(spectrogram)
        dft = np.abs(np.fft.rfft(onset_signal))
        freqs = np.fft.rfftfreq(len(onset_signal), d=self.hop_size/self.sr)
        valid_idx = np.where((freqs * 60 >= self.bpm_range[0]) & (freqs * 60 <= self.bpm_range[1]))
        tempo_idx = valid_idx[0][np.argmax(dft[valid_idx])]
        estimated_bpm = freqs[tempo_idx] * 60
        return estimated_bpm
