import librosa
import numpy as np
import csv
import os
import sys

from src.featurizer.Spectral_Rolloff_Featurizer import SpectralRolloff
from src.featurizer.Spectral_Centroid_Featurizer import SpectralCentroid
from src.featurizer.Spectral_Bandwidth_Featurizer import SpectralBandwidth
from src.featurizer.Spectral_Contrast_Featurizer import SpectralContrast
from src.featurizer.Spectral_Flux_Featurizer import SpectralFlux
from src.featurizer.RMS_Featurizer import RMSComputation
from src.featurizer.Dynamic_Range_Featurizer import DynamicRangeComputation
from src.featurizer.Instrumentalness_Featurizer import InstrumentalnessComputation
from src.featurizer.Audio_Splitter import Audio_Splitter
from src.featurizer.Beats_Per_Minute_Featurizer import Tempo_Estimator
from src.featurizer.Key_and_Scale_Featurizer import Key_Estimator


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
        self.audio_splitter = Audio_Splitter()

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
        vocal_signal, non_vocal_signal = self.audio_splitter.split_audio(signal)

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
    
    """Collapse the features into n sections for recommendation"""
    def collapse_into_sections(self, feature, n_sections=8):
        """
        Collapses a feature into `n_sections` by computing the mean.

        Parameters:
            feature (ndarray): The input feature array (num_rows, num_features).
            n_sections (int): Number of sections to divide the array into.

        Returns:
            collapsed_array (ndarray): (n_sections, 1), each section represented by its mean.
        """
        num_rows = feature.shape[0]
        section_size = num_rows // n_sections 

        collapsed_array = []

        for i in range(n_sections):
            start = i * section_size
            end = num_rows if i == n_sections - 1 else start + section_size

            section_mean = np.mean(feature[start:end], axis=0)
            collapsed_array.append(np.mean(section_mean))

        return np.array(collapsed_array).reshape(n_sections, 1)

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
        collapsed_rolloff = self.collapse_into_sections(spectral_rolloff)

        spectral_centroid, mean_centroid, _ = self.spectral_centroid.compute_spectral_centroids_mean(divided_stft_magnitudes)
        collapsed_centroid = self.collapse_into_sections(spectral_centroid)

        spectral_bandwidth, mean_bandwidth, _ = self.spectral_bandwidth.compute_spectral_bandwidth_mean(divided_stft_magnitudes, spectral_centroid)
        collapsed_bandwidth = self.collapse_into_sections(spectral_bandwidth)

        spectral_contrast, mean_contrast, _ = self.spectral_contrast.compute_spectral_contrast_mean(divided_stft_magnitudes)
        collapsed_contrast = self.collapse_into_sections(spectral_contrast)

        rms_values, mean_rms = self.rms_computation.compute_rms(divided_stft_magnitudes)
        collapsed_rms = self.collapse_into_sections(rms_values)

        dynamic_range, mean_dynamic_range = self.dynamic_range.compute_dynamic_range(divided_stft_magnitudes, rms_values)
        collapsed_dynamic_range = self.collapse_into_sections(dynamic_range)

        spectral_flux, mean_spectral_flux = self.spectral_flux.compute_spectral_flux_mean(divided_stft_magnitudes)
        collapsed_spectral_flux = self.collapse_into_sections(spectral_flux)

        major_key, minor_key = self.key_estimator.estimate_keys(signal)

        #for instrumentalness we need the RMS of vocal
        rms_vocal, _ = self.rms_computation.compute_rms(div_stft_vocal_mag)
        instrumentalness, mean_instrumentalness = self.instrumentalness.compute_instrumentalness(rms_values, rms_vocal)
        collapsed_instrumentalness = self.collapse_into_sections(instrumentalness)

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

        collaped_features = {
            "collapsed_rolloff": collapsed_rolloff,
            "collapsed_centroid": collapsed_centroid,
            "collapsed_bandwidth": collapsed_bandwidth,
            "collapsed_contrast": collapsed_contrast,
            "collapsed_rms": collapsed_rms,
            "collapsed_flux": collapsed_spectral_flux,
            "collapsed_dynamic_range": collapsed_dynamic_range,
            "collapsed_instrumentalness": collapsed_instrumentalness,
            "major_key": major_key,
            "minor_key": minor_key,
            "bpm": round(bpm)
        } 

        features = {
            "mean_spectral_rolloff": mean_rolloff,
            "mean_spectral_centroid": mean_centroid,
            "mean_spectral_bandwidth": mean_bandwidth,
            "mean_spectral_contrast": mean_contrast,
            "mean_rms": mean_rms,
            "mean_dynamic_range": mean_dynamic_range,
            "mean_instrumentalness": mean_instrumentalness,
            "mean_spectral_flux": spectral_flux,
            "major_key": major_key,
            "minor_key": minor_key,
            "bmp": round(bpm)
        }   
        
        return collaped_features

    def write_features_to_csv(self, track_name, features, csv_filepath="src/featurizer/test.csv"):
        """
        Writes feature dictionary data into a CSV file, and seperates the data by section for the recommendation algo

        Parameters:
            track_name (str): The name of the track (not included in the features dictionary).
            features (dict): Dictionary containing track features.
            csv_filepath (str): Path to the CSV file.
        """

        # Extract feature names and expand list-based features
        expanded_fieldnames = ["track_name"]  # Start with track name as the first column

        # Iterate through the dictionary keys and dynamically create column names
        for key, value in features.items():
            if isinstance(value, np.ndarray) and value.shape[0] == 8:  # If the feature has 8 sections
                expanded_fieldnames.extend([f"{key}_{i+1}" for i in range(8)])
            else:  # Non-array features like BPM, key, etc.
                expanded_fieldnames.append(key)

        # Ensure directory exists
        os.makedirs(os.path.dirname(csv_filepath), exist_ok=True)

        # Open CSV file in append mode ('a' means add new rows)
        file_exists = os.path.exists(csv_filepath)
        with open(csv_filepath, mode="a", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=expanded_fieldnames)

            # If the file is new, write the headers first
            if not file_exists:
                writer.writeheader()

            # Convert NumPy arrays to lists before writing
            expanded_features = {"track_name": track_name}  # Store the track name

            for key, value in features.items():
                if isinstance(value, np.ndarray) and value.shape[0] == 8:  # If it's an array with 8 sections
                    for i in range(8):
                        expanded_features[f"{key}_{i+1}"] = value[i][0]  # Extract each value
                else:  # Directly store non-array features
                    expanded_features[key] = value

            # Write the features dictionary as a row
            writer.writerow(expanded_features)

        print(f"Features for '{track_name}' successfully written to {csv_filepath}")

def main_directory(directory = "src/deezer_previews/"):
    feat = Featurizer()
    for audio_file in os.scandir(directory):
        #extract name
        # _name = f"{audio_file.path}".split("/")[2].split(".")[0].split("(")[0]
        _name = f"{audio_file.path}".split("/")[2]

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
        print(line)
        feat.write_features_to_csv(line)

def main_audio_file(audio_file_path = "src/audio/"):
    # init featurizer
    feat = Featurizer()
    #extract name
    _name = f"{audio_file_path}".split("/")[2].split(".")[0].split("(")[0]
    # _name = _name.split("preview_")[1]
    song_name = {"track_name": _name}
    print(f"Currently Featurizing: {_name}")

    signal, sr, vocal_signal, _ = feat.process_audio(audio_file_path, sampling_rate=44100)

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
    
    #mash the dictionaries together
    line = song_name | features
    # feat.write_features_to_csv(line)

if __name__ == "__main__":
    main_directory("src/deezer_gooner/")