import librosa
import numpy as np
import scipy.linalg
from scipy.stats import zscore

class Key_Estimator:
    major_profile = np.asarray([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
    minor_profile = np.asarray([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
    KEY_MAPPING = {0: "C", 1: "C#/Db", 2: "D", 3: "D#/Eb", 4: "E", 5: "F", 
                   6: "F#/Gb", 7: "G", 8: "G#/Ab", 9: "A", 10: "A#/Bb", 11: "B"}

    def __init__(self, sr = 44100):
       self.major_profile = zscore(self.major_profile)
       self.major_profile_norm = scipy.linalg.norm(self.major_profile)
       self.major_profile = scipy.linalg.circulant(self.major_profile)
       
       self.minor_profile = zscore(self.minor_profile)
       self.minor_profile_norm = scipy.linalg.norm(self.minor_profile)
       self.minor_profile = scipy.linalg.circulant(self.minor_profile)
       self.sr = sr
       
    def separate_signal(self, signal):
        harmonic, _ = librosa.effects.hpss(signal)
        return harmonic

    def compute_notes(self, signal):
        return librosa.feature.chroma_stft(y=signal, sr=self.sr)
    
    def get_pitch_class_distribution(self, notes):
        return notes.sum(axis=1)
    
    def get_coefficients(self, pitch_class_distribution):
        pitch_class_distribution = zscore(pitch_class_distribution)
        pitch_class_distribution_norm = scipy.linalg.norm(pitch_class_distribution)

        major_coefficients = self.major_profile.T.dot(pitch_class_distribution) / self.major_profile_norm / pitch_class_distribution_norm
        minor_coefficients = self.minor_profile.T.dot(pitch_class_distribution) / self.minor_profile_norm / pitch_class_distribution_norm

        return major_coefficients, minor_coefficients
    
    def estimate_keys(self, signal):
        harmonic = self.separate_signal(signal)
        notes = self.compute_notes(harmonic)
        pcd = self.get_pitch_class_distribution(notes)
        coefficients = self.get_coefficients(pcd)
        
        major_key = f'{self.KEY_MAPPING[np.argmax(coefficients[0])]} Major'
        minor_key = f'{self.KEY_MAPPING[np.argmax(coefficients[1])]} Minor'

        return major_key, minor_key
