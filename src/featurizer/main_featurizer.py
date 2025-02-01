import librosa
import numpy as np

"""main featurizer module"""

"""audio processor
taken from matthew baleanu and Mohamad-Hassan Bahsoun
16khz downsample (default 22.05khz, spotify audio is 44.1khz.)
default sampling rate set to 16khz as per @bahsoun"""
def process_audio(audio_file_path, target_sample_rate=16000):
    """load the audio and sample it at the target rate. 
    librosa.load converts the audio file into a time series at the desired sampling rate """
    signal, sampling_rate = librosa.load(audio_file_path, sr=target_sample_rate, mono=True)
    """normalize the amplitude of the signal."""
    signal = signal / np.max(np.abs(signal))
    """stft signal for feature computation. probably will be moved. """
    stft_signal = librosa.stft(signal, window='hann')
    return signal, stft_signal, sampling_rate

"""Signal Divider Based on BPM
    as suggested by MVM, the signal we divide up the signal into bins and compute a window size in order to get
    variance for our feature, this way we can determine how relevant they would be for classification/recommendation."""
def divide_signal(signal, bpm, sampling_rate, beats_per_win = 4):
    """process is as such:
    1. get global tempo (bpm)
    2. convert that to beat segments
    3. use it to divide up the song."""
    beat_duration = 60/bpm
    song_length_seconds = len(signal)/sampling_rate
    beat_count = song_length_seconds/beat_duration
    
    """once beat count is computed, compute the window size as a fixed multiple of the beat count
    Round up division on beat_count/beats_per_win to compute the window count. 
    To calculate the window size: the length of the signal is seconds * samples, as that is an audio time series. The window size would 
    therefore be the sample length of len(signal)/window_count rounded up, in order to contain all samples."""
    window_count = int(np.ceil(beat_count/beats_per_win))
    window_size = int(np.ceil(len(signal)/window_count))
    
    """to divide the signal we pad the original signal with zeroes at the end until it is of the proper length
    for consistency and then reshape it."""
    
    divided_signal = np.pad(signal,
                            (0, window_count*window_size-len(signal)),
                            mode="constant",
                            constant_values=0)
    
    """now we must reshape the signal."""
    divided_signal = divided_signal.reshape(window_count, window_size)
    return divided_signal, window_size, window_count

"""need to STFT invidual pieces"""
def divide_stft(divided_signal):
    """sample STFT calculation is necessary in order to perform preallocation for efficiency"""
    x, y = librosa.stft(divided_signal[0]).shape
    divided_stft_signal = np.zeros((divided_signal.shape[0], x, y), dtype=np.complex128)
    divided_stft_magnitudes = np.zeros((divided_signal.shape[0], x, y))
    for i in range(divided_signal.shape[0]): 
        stft_slice = librosa.stft(divided_signal[i])
        divided_stft_signal[i] = stft_slice
        divided_stft_magnitudes[i] = np.abs(stft_slice)

    return divided_stft_signal, divided_stft_magnitudes