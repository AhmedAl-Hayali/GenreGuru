import librosa
import numpy as np
import csv
import os
import sys

from Spectral_Rolloff_Featurizer import SpectralRolloff
from Spectral_Centroid_Featurizer import SpectralCentroid
from Spectral_Bandwidth_Featurizer import SpectralBandwidth
from Spectral_Contrast_Featurizer import SpectralContrast
from Spectral_Flux_Featurizer import SpectralFlux
from RMS_Featurizer import RMSComputation
from Dynamic_Range_Featurizer import DynamicRangeComputation
from Instrumentalness_Featurizer import InstrumentalnessComputation
from BPM_Featurizer import *
from Audio_Splitter import Audio_Splitter
from Beats_Per_Minute_Featurizer import Tempo_Estimator
from Key_and_Scale_Featurizer import Key_Estimator


class Featurizer:
    """
    Main Featurizer class.
    Handles preparing the input, passing the signal into feature computation modules.
    """

    def __init__(self, target_sample_rate=44100, n_bands=7):
        """
        Initialize the Featurizer class.

        Parameters:
            target_sample_rate (int): Sampling rate for audio processing (default is 44.1kHz).
            n_bands (int): Number of frequency bands for spectral contrast (default: 7).
        """
        self.target_sample_rate = target_sample_rate
        self.n_bands = n_bands

        # Initialize feature extraction classes
        self.spectral_rolloff = SpectralRolloff(self.target_sample_rate)
        self.spectral_centroid = SpectralCentroid(self.target_sample_rate)
        self.spectral_bandwidth = SpectralBandwidth(self.target_sample_rate)
        self.spectral_contrast = SpectralContrast(self.n_bands)
        self.spectral_flux = SpectralFlux()
        self.rms_computation = RMSComputation()
        self.dynamic_range = DynamicRangeComputation()
        self.instrumentalness = InstrumentalnessComputation()
        self.key_estimator = Key_Estimator()

    """Audio Processor
    Taken from Matthew Baleanu and Mohamad-Hassan Bahsoun
    16kHz downsample (default 22.05kHz, Spotify audio is 44.1kHz.)
    Default sampling rate set to 16kHz as per @bahsoun.
    """
    def process_audio(self, audio_file_path, sampling_rate=44100):
        """
        Loads the audio file, normalizes it, and computes the STFT.
        
        Parameters:
            audio_file_path (str): Path to the audio file.
        
        Returns:
            signal (ndarray): Normalized audio time series.
            stft_signal (ndarray): STFT of the signal.
            sampling_rate (int): Sampling rate of the audio.
        """
        # Load the audio file
        signal, sampling_rate = librosa.load(audio_file_path, sr=self.target_sample_rate, mono=True)
        
        # Normalize the amplitude of the signal
        signal = signal / np.max(np.abs(signal))
        
        #split the audio into vocal and non-vocal
        AudioSplitter = Audio_Splitter()
        vocal_signal, non_vocal_signal = AudioSplitter.split_audio(signal)

        # Compute STFT for feature extraction
        # stft_signal = librosa.stft(signal, window='hann')

        return signal, sampling_rate, vocal_signal, non_vocal_signal

    """Signal Divider Based on BPM
    As suggested by MVM, the signal is divided into bins, and a window size is computed
    to get variance for features, making them more relevant for classification/recommendation.
    """
    def divide_signal(self, signal, bpm, windows_per_beat=4):
        """
        Splits the audio signal into fixed-length windows based on BPM.
        
        Parameters:
            signal (ndarray): Audio time-series data.
            bpm (float): Beats per minute of the track.
            windows_per_beat (int): Number of windows per beat (default: 4).
        
        Returns:
            divided_signal (ndarray): 2D array of segmented signal.
            window_size (int): Size of each window in samples.
            window_count (int): Number of windows.
        """
        beat_duration = 60 / bpm
        song_length_seconds = len(signal) / self.target_sample_rate
        beat_count = song_length_seconds / beat_duration

        # Compute window count as beats * windows_per_beat
        window_count = int(np.ceil(beat_count * windows_per_beat))
        window_size = int(np.ceil(len(signal) / window_count))

        # Pad the signal to make it evenly divisible
        divided_signal = np.pad(signal,
                                (0, window_count * window_size - len(signal)),
                                mode="constant",
                                constant_values=0)

        # Reshape into windowed segments
        divided_signal = divided_signal.reshape(window_count, window_size)
        return divided_signal, window_size, window_count

    """Need to STFT individual pieces"""
    def divide_stft(self, divided_signal):
        """
        Computes the STFT for each windowed segment of the signal.
        
        Parameters:
            divided_signal (ndarray): 2D array of windowed audio segments.
        
        Returns:
            divided_stft_signal (ndarray): 3D array of complex STFT values.
            divided_stft_magnitudes (ndarray): 3D array of STFT magnitude values.
        """
        # Sample STFT calculation is necessary to perform preallocation for efficiency
        x, y = librosa.stft(divided_signal[0]).shape
        divided_stft_signal = np.zeros((divided_signal.shape[0], x, y), dtype=np.complex128)
        divided_stft_magnitudes = np.zeros((divided_signal.shape[0], x, y))

        for i in range(divided_signal.shape[0]): 
            stft_slice = librosa.stft(divided_signal[i])
            divided_stft_signal[i] = stft_slice
            divided_stft_magnitudes[i] = np.abs(stft_slice)

        return divided_stft_signal, divided_stft_magnitudes
    
    """Compute All Features"""
    def compute_features(self, divided_stft_magnitudes, div_stft_vocal_mag, signal, bpm):
        """
        Computes all features from the processed STFT magnitudes and divided signal.

        Parameters:
            divided_stft_magnitudes (ndarray): 3D array of STFT magnitudes.
            divided_signal (ndarray): 2D array of segmented signal.
            bpm (float): Beats per minute of the track.

        Returns:
            features (dict): Dictionary containing all extracted features. 
        """
        # Compute each feature
        # need to add BPM
        spectral_rolloff, mean_rolloff = self.spectral_rolloff.compute_frequency_range(divided_stft_magnitudes)
        spectral_centroid, mean_centroid, _ = self.spectral_centroid.compute_spectral_centroids_mean(divided_stft_magnitudes)
        spectral_bandwidth, mean_bandwidth, _ = self.spectral_bandwidth.compute_spectral_bandwidth_mean(divided_stft_magnitudes, spectral_centroid)
        spectral_contrast, mean_contrast, _ = self.spectral_contrast.compute_spectral_contrast_mean(divided_stft_magnitudes)
        rms_values, mean_rms = self.rms_computation.compute_rms(divided_stft_magnitudes)
        dynamic_range, mean_dynamic_range = self.dynamic_range.compute_dynamic_range(divided_stft_magnitudes, rms_values)
        major_key, minor_key = self.key_estimator.estimate_keys(signal)

        #for instrumentalness we need the RMS of vocal
        rms_vocal, _ = self.rms_computation.compute_rms(div_stft_vocal_mag)
        instrumentalness, mean_instrumentalness = self.instrumentalness.compute_instrumentalness(rms_values, rms_vocal)

        # Store features in
        # features = {
        #     "spectral_rolloff": spectral_rolloff,
        #     "mean_spectral_rolloff": mean_rolloff,
        #     "spectral_centroid": spectral_centroid,
        #     "mean_spectral_centroid": mean_centroid,
        #     "spectral_bandwidth": spectral_bandwidth,
        #     "mean_spectral_bandwidth": mean_bandwidth,
        #     "spectral_contrast": spectral_contrast,
        #     "mean_spectral_contrast": mean_contrast,
        #     "rms": rms_values,
        #     "mean_rms": mean_rms,
        #     "dynamic_range": dynamic_range,
        #     "mean_dynamic_range": mean_dynamic_range,
        #     "instrumentalness": instrumentalness,
        #     "mean_instrumentalness": mean_instrumentalness,
        #     "major_key": major_key,
        #     "minor_key": minor_key,
        #     "bmp": round(bpm)
        # }

        features = {
            "mean_spectral_rolloff": mean_rolloff,
            "mean_spectral_centroid": mean_centroid,
            "mean_spectral_bandwidth": mean_bandwidth,
            "mean_spectral_contrast": mean_contrast,
            "mean_rms": mean_rms,
            "mean_dynamic_range": mean_dynamic_range,
            "mean_instrumentalness": mean_instrumentalness,
            "major_key": major_key,
            "minor_key": minor_key,
            "bmp": round(bpm)
        }   
        
        return features

    def write_to_csv(self, track_features, csv_filepath="src/featurizer/featurized_music.csv"):
        "writes audio features to a .csv file"

        # check if we need to create the file, and then check if we need to create fieldnames
        os.makedirs(os.path.dirname(csv_filepath), exist_ok=True)
        file_exists = os.path.exists(csv_filepath)
        with open(csv_filepath, mode='a', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'track_name',
                'mean_spectral_rolloff',
                'mean_spectral_centroid', 
                'mean_spectral_bandwidth',
                'mean_spectral_contrast',
                'mean_rms',
                'mean_dynamic_range',
                'mean_instrumentalness',
                'major_key',
                'minor_key',
                'bmp'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()
            writer.writerow({
                'track_name': track_features['track_name'],
                'mean_spectral_rolloff': round(track_features['mean_spectral_rolloff'], 6),
                'mean_spectral_centroid': round(track_features['mean_spectral_centroid'], 6),
                'mean_spectral_bandwidth': round(track_features['mean_spectral_bandwidth'], 6),
                'mean_spectral_contrast': round(track_features['mean_spectral_contrast'], 6),
                'mean_rms': round(track_features['mean_rms'], 6),
                'mean_dynamic_range': round(track_features['mean_dynamic_range'], 6),
                'mean_instrumentalness': round(track_features['mean_instrumentalness'], 6),
                'major_key': track_features['major_key'],
                'minor_key': track_features['minor_key'],
                'bmp': track_features['bmp']
            })

# def main(audio_file):
#     # init featurizer
#     feat = Featurizer()
#     #extract name
#     _name = f"{audio_file}".split("/")[2].split(".")[0].split("(")[0]
#     # _name = _name.split("preview_")[1]
#     song_name = {"track_name": _name}
#     print(f"Currently Featurizing: {_name}")

#     signal, sr, vocal_signal, _ = feat.process_audio(audio_file, sampling_rate=44100)

#     #compute the bpmn
#     tempo = Tempo_Estimator(sr = sr)
#     bpm = tempo.estimate_tempo(signal)
    
#     #divide the signal
#     div_signal, _, _ = feat.divide_signal(signal, bpm)
#     div_stft_signal, div_stft_mag = feat.divide_stft(div_signal)

#     #divide signals of the vocal for instrumentalness
#     div_vocal, _, _ = feat.divide_signal(vocal_signal, bpm)
#     _, div_stft_vocal_mag = feat.divide_stft(div_vocal)

#     features = feat.compute_features(div_stft_mag, div_stft_vocal_mag, signal, bpm)
    
#     #mash the dictionaries together
#     line = song_name | features
#     feat.write_to_csv(line)

def main(directory):
    # init featurizer
    feat = Featurizer()

    #modified to operate over a directory instead of input file
    for audio_file in os.scandir(directory):
        #extract name
        _name = f"{audio_file.path}".split("/")[2].split(".")[0].split("(")[0]
        # _name = _name.split("preview_")[1]
        song_name = {"track_name": _name}
        print(f"Currently Featurizing: {_name}")

        signal, sr, vocal_signal, _ = feat.process_audio(audio_file, sampling_rate=44100)

        #compute the bpmn
        tempo = Tempo_Estimator(sr = sr)
        bpm = tempo.estimate_tempo(signal)
        
        #divide the signal
        div_signal, _, _ = feat.divide_signal(signal, bpm)
        div_stft_signal, div_stft_mag = feat.divide_stft(div_signal)

        #divide signals of the vocal for instrumentalness
        div_vocal, _, _ = feat.divide_signal(vocal_signal, bpm)
        _, div_stft_vocal_mag = feat.divide_stft(div_vocal)

        features = feat.compute_features(div_stft_mag, div_stft_vocal_mag, signal, bpm)

        line = song_name | features
        feat.write_to_csv(line)
    
# if __name__ == "__main__":
#     main("src/audio/Adele - Hello (Official Music Video).wav")

if __name__ == "__main__":
    main("src/deezer_previews/")