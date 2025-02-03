import librosa
import numpy as np

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

    """Audio Processor
    Taken from Matthew Baleanu and Mohamad-Hassan Bahsoun
    16kHz downsample (default 22.05kHz, Spotify audio is 44.1kHz.)
    Default sampling rate set to 16kHz as per @bahsoun.
    """
    def process_audio(self, audio_file_path):
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
        vocal_signal, non_vocal_signal = AudioSplitter.separate(signal)

        # Compute STFT for feature extraction
        stft_signal = librosa.stft(signal, window='hann')

        return signal, stft_signal, sampling_rate, vocal_signal, non_vocal_signal

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
    def compute_features(self, divided_stft_magnitudes, divided_signal, div_stft_vocal, div_stft_non_vocal_mag):
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
        dynamic_range, mean_dynamic_range = self.dynamic_range.compute_dynamic_range(divided_signal, rms_values)
        instrumentalness, mean_instrumentalness = self.instrumentalness.compute_instrumentalness(rms_values, rms_values)

        # Store features in
        features = {
            "spectral_rolloff": spectral_rolloff,
            "mean_spectral_rolloff": mean_rolloff,
            "spectral_centroid": spectral_centroid,
            "mean_spectral_centroid": mean_centroid,
            "spectral_bandwidth": spectral_bandwidth,
            "mean_spectral_bandwidth": mean_bandwidth,
            "spectral_contrast": spectral_contrast,
            "mean_spectral_contrast": mean_contrast,
            "rms": rms_values,
            "mean_rms": mean_rms,
            "dynamic_range": dynamic_range,
            "mean_dynamic_range": mean_dynamic_range,
            "instrumentalness": instrumentalness,
            "mean_instrumentalness": mean_instrumentalness
        }
        
        return features


def main(audio_file):
    feat = Featurizer()

    # process the audio
    signal, whole_stft, sr, vocal_signal, non_vocal_signal = feat.process_audio(audio_file)
    #compute the bpmn
    bpm = compute_bpm(signal, sr)

    div_s, win_size, win_count = feat.divide_signal(signal, bpm)
    div_stft_s, div_stft_mag = feat.divide_stft(div_s)

    #divide signals of the vocal and non-vocal
    div_vocal, _, _ = feat.divide_signal(vocal_signal, bpm)
    _, div_stft_vocal_mag = feat.divide_stft(div_vocal)

    div_non_vocal, _, _ = feat.divide_signal(non_vocal_signal, bpm)
    _, div_stft_non_vocal_mag = feat.divide_stft(div_non_vocal)



    features = feat.compute_features(div_stft_mag,div_stft_s, div_stft_vocal_mag, div_stft_non_vocal_mag)


    print("") #spacer
    for key, value in features.items():
        if type(value) == float:
            print(f"{key}: ({type(value).__name__})\n")
        else:
            print(f"{key}: ({type(value).__name__}) ({value.shape})\n")


if __name__ == "__main__":
    main("../audio/katy.mp3")

