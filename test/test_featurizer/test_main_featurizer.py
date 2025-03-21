import pytest
import random
import wave
import numpy as np
import os
from src.featurizer.main_featurizer import Featurizer

AUDIO_DIR = "src/deezer_previews"

#compute the duration of the song in seconds in order to assertain the length of signal
def compute_expected_size(file_path, sampling_rate):
    with wave.open(file_path, 'rb') as wav_file:
        frames = wav_file.getnframes()  #Total number of audio frames
        framerate = wav_file.getframerate()  #Sample rate (frames per second)
        duration = frames / framerate
        return int(duration*sampling_rate) #typecast for typematching, return the expected size

#generate random inputs and outputs for isolation
AUDIO_FILE_PATH = os.path.join(AUDIO_DIR, random.choice(os.listdir(AUDIO_DIR)))

SAMPLING_RATE = 44100
BANDS = 7
DURATION = 10
FREQUENCY_BINS = 1025
TIME_FRAMES = 512

@pytest.fixture
def featurizer():
    return Featurizer(SAMPLING_RATE, BANDS)

def test_init(featurizer):
    assert featurizer.target_sample_rate == SAMPLING_RATE, (
        f"sample rate mismatch in init, SAMPLING_RATE IS: {SAMPLING_RATE}, target_sampling_rate of featurizer is: {featurizer.target_sample_rate}")
    
    assert featurizer.n_bands == BANDS, (
        f"sample rate mismatch in init, BANDS IS: {BANDS}, n_bands of featurizer is: {featurizer.n_bands}")


def process_audio(featurizer):
    return featurizer.process_audio(AUDIO_FILE_PATH, SAMPLING_RATE)

"""audio processor module test  of main featurizer
Parameters:
    audio_file_path (str): file path of the audio file
    sampling_rate(int): sampling rate for the algo

Returns:
    signal (ndarray): floating point time series representation of song. 
    - the size is length of the song (seconds) * sampling rate, which gives the number of frequency samples
    sampling_rate (int): value is the same as input
    vocal_signal (ndarray): floating point time series representation of vocal portion
    non_vocal_signal (ndarray):floating point time series representation of instrumental portion"""
def test_process_audio(featurizer):
    #random sampling of an audio file
    signal, sampling_rate_after, vocal_signal, non_vocal_signal = featurizer.process_audio(AUDIO_FILE_PATH, SAMPLING_RATE)
    
    #compute the length of the audio file to assert ndarray shape. Vocal and non-vocal signal share the same duration
    expected_size = compute_expected_size(AUDIO_FILE_PATH, SAMPLING_RATE)

    #for input, it is just an audio file path, so we check for string type.
    assert isinstance(AUDIO_FILE_PATH, str), f"Expected str, got {type(AUDIO_FILE_PATH)}"

    """for signal, we need to check for ndarray, contains floats, and shape. """
    #first, check for ndarray that contains floats:
    assert isinstance(signal, np.ndarray) and np.issubdtype(signal.dtype, np.floating), (
        f"Expected numpy array of floats, got {type(signal)} with dtype "
        f"{getattr(signal, 'dtype', 'N/A')}")  #print type if not array
    
    #second we check for the shape:
    assert signal.shape[0] == expected_size, (f"Expected shape {expected_size}, got {signal.shape}")

    """sampling_rate we check for type, and for no change between smapling_rate before and after."""
    assert isinstance(SAMPLING_RATE, int), f"Expected int, got {type(SAMPLING_RATE)}"
    assert SAMPLING_RATE == sampling_rate_after, f"SAMPLING_RATE MISMATCH,  SAMPLING_RATE: {SAMPLING_RATE} != sampling_rate_after: {sampling_rate_after}"

    """vocal signal we check for ndarray, contains flats, and shape."""
    #first, check for ndarray that contains floats:
    assert isinstance(vocal_signal, np.ndarray) and np.issubdtype(vocal_signal.dtype, np.floating), (
        f"Expected numpy array of floats, got {type(vocal_signal)} with dtype "
        f"{getattr(vocal_signal, 'dtype', 'N/A')}")  #print type if not array
    
    #second we check for the shape:
    assert vocal_signal.shape[0] == expected_size, (f"Expected shape {expected_size}, got {vocal_signal.shape}")

    """non-vocal signal we check for ndarray, contains flats, and shape."""
    #first, check for ndarray that contains floats:
    assert isinstance(non_vocal_signal, np.ndarray) and np.issubdtype(non_vocal_signal.dtype, np.floating), (
        f"Expected numpy array of floats, got {type(non_vocal_signal)} with dtype "
        f"{getattr(non_vocal_signal, 'dtype', 'N/A')}")  #print type if not array
    
    #second we check for the shape:
    assert non_vocal_signal.shape[0] == expected_size, (f"Expected shape {expected_size}, got {non_vocal_signal.shape}")

#isolate the inputs and outputs
SIGNAL = np.random.uniform(-1, 1, (DURATION * SAMPLING_RATE)).astype(np.float64)
BPM = 60.0
WINDOWS_PER_BEAT = 4

def divide_signal(featurizer):
    return featurizer.divide_signal(SIGNAL, BPM, WINDOWS_PER_BEAT)

"""test for the divide_signal function of main featurizer:
parameters: 
    signal (ndarray of floats, shape = (song_duration*sampling_rate,)): Audio time-series data, normalized monochannel audio signal
    - test for numpy array of floats
    - check for flat shape
    bpm (float): Beats per minute of the track.
    - test for float
    windows_per_beat (int): Number of windows per beat (default: 4).
    - test for int
Returns:
    divided_signal (ndarray, shape = (windows, window_size)): 2D array of segmented signal.
    - test for numpy array of floats
    - test for shape (windows * window_size >= signal.shape due to round up)
    window_size (int, #samples in signal/windows_per_beat rounded up): Size of each window in samples.
    - test for int
    window_count (int, beat_count * windows_per_beat rounded up): Number of windows.
    - test for int"""
def test_divide_signal(featurizer):
    divided_signal, window_size, window_count = featurizer.divide_signal(SIGNAL, BPM, WINDOWS_PER_BEAT)
    """check for input signal integrity"""
    assert isinstance(SIGNAL, np.ndarray) and np.issubdtype(SIGNAL.dtype, np.floating), (
        f"SIGNAL Expected numpy array of floats, got {type(SIGNAL)} with dtype "
        f"{getattr(SIGNAL, 'dtype', 'N/A')}")  #print type if not array
    
    #check for SIGNAL being flat, and therefore monochannel:
    assert len(SIGNAL.shape) == 1, (f"SIGNAL has the wrong shape, is not flat: {SIGNAL.shape}")
    
    """check that BPM is a float:"""
    assert isinstance(BPM, float), f"BPM Expected float, got {type(BPM)}"

    """check that WINDOWS_PER_BEAT is int:"""
    assert isinstance(WINDOWS_PER_BEAT, int), f"WINDOWS_PER_BEAT Expected int, got {type(WINDOWS_PER_BEAT)}"

    """check divided signal is 2D array of floats"""
    #check that it is an numpy array of floats
    assert isinstance(divided_signal, np.ndarray) and np.issubdtype(divided_signal.dtype, np.floating), (
        f"divided_signal expected numpy array of floats, got {type(divided_signal)} with dtype "
        f"{getattr(divided_signal, 'dtype', 'N/A')}")  #print type if not array

    """check that window_count and window_size are integers:"""
    assert isinstance(window_size, int), f"window_size expected int, got {type(window_size)}"
    assert isinstance(window_count, int), f"window_count expected int, got {type(window_count)}"

    """now test that divided_signal has the right shape"""
    assert len(divided_signal == 2), f"divided_signal is not 2D, is {len(divided_signal)}D"

    assert divided_signal.shape[0] == window_count, (
        f"divided_signal.shape[0] != window_count, got {divided_signal.shape[0]}")

    assert divided_signal.shape[1] == window_size, (
        f"divided_signal.shape[1] != window_size, got {divided_signal.shape[1]}")
    
    """as we pad the signal we also must know that window_count * window_size >= len(SIGNAL):"""
    assert divided_signal.shape[0] * divided_signal.shape[1] >= len(SIGNAL), (
        f"incorrect divided_signal_length, divided signal length is: {divided_signal.shape[0] * divided_signal.shape[1]}\
        which is less than SIGNAL's length: {len(SIGNAL)}")
    
WINDOWS = 12
WINDOW_SIZE = 6000 #is in samples
#divided signal is 2D d arr, with shape (windows, data), we generate a synthetic normalized signal:
DIVIDED_SIGNAL = np.random.uniform(-1, 1, (WINDOWS, WINDOW_SIZE)).astype(np.float64)
def divide_stft(featurizer): 
    return featurizer.divide_stft(DIVIDED_SIGNAL)

"""tests for divide_stft
parameters:
    divided_signal (3d array, shape = (WINDOWS, FREQUENCY_BINS, TIME_FRAMES)
    - test for 2d of floats
returns:
    divided_stft_signal (ndarray): 3D array of complex STFT values.
    -test for 3D, test for complex values, test for window_count = divided signal = divided_stft_magnitudes
    divided_stft_magnitudes (ndarray): 3D array of STFT magnitude values.
    -test for 3D, test for non-negative vlaues (magnitudes), test shape = divided_stft_signal"""
def test_divide_stft(featurizer):
    divided_stft_signal, divided_stft_magnitudes = featurizer.divide_stft(DIVIDED_SIGNAL)
    """type and shape check on DIVIDED_SIGNAL:"""
    assert isinstance(DIVIDED_SIGNAL, np.ndarray) and np.issubdtype(DIVIDED_SIGNAL.dtype, np.floating), (
        f"Expected numpy array of floats, got {type(DIVIDED_SIGNAL)} with dtype "
        f"{getattr(DIVIDED_SIGNAL, 'dtype', 'N/A')}")  #print type if not array
    assert len(DIVIDED_SIGNAL.shape)==2, f"DIVIDED_SIGNAL needs to be 2D, is {len(DIVIDED_SIGNAL)}D"

    """first, check that div_stft_signal is 3D:"""
    assert len(divided_stft_signal.shape)==3, f"divided_stft_signal needs to be 3D, is {len(divided_stft_signal)}D"
    """check window count integrity:"""
    assert divided_stft_signal.shape[0] == DIVIDED_SIGNAL.shape[0],\
        f"window count integrity violated, div_stft_signal: {divided_stft_signal.shape[0]} != DIVIDED_SIGNAL: {DIVIDED_SIGNAL.shape[0]}"
    """check that it has the same shape as the magnitudes:"""
    assert divided_stft_signal.shape == divided_stft_magnitudes.shape, (
        f"Shape mismatch: divided_stft_signal:{divided_stft_signal.shape} != divided_stft_magnitudes: {divided_stft_magnitudes.shape}")

    """now we check for the integrity of the data contained in div_stft, div_stft_mags"""
    assert np.issubdtype(divided_stft_signal.dtype, np.complexfloating), ( # check for complex values as STFT
        f"divided_stft_signal expected complex dtype, got {divided_stft_signal.dtype}")
    
    # check for non-negative floats
    assert np.issubdtype(divided_stft_magnitudes.dtype, np.floating) and np.all(divided_stft_magnitudes >= 0), (
        f"divided_stft_magnitudes must contain non-negative floats (STFT magnitudes), "
        f"got dtype={divided_stft_magnitudes.dtype} with min={np.min(divided_stft_magnitudes):.2f}")
    
    # check the magnitudes roughly align:
    assert np.allclose(np.abs(divided_stft_signal), divided_stft_magnitudes), f"Magnitudes do not match absolute values of complex STFT"


def test_collapse_into_sections(featurizer):
    """Test collapse_into_sections with a known input."""
    spectral_centroid = np.random.rand(171, 16)

    collapsed = featurizer.collapse_into_sections(spectral_centroid)

    assert collapsed.shape == (8, 1), "Collapsed output shape is incorrect"
    assert np.isfinite(collapsed).all(), "Output contains NaN or infinite values"

    section_size = 171 // 8
    for i in range(8):
        start = i * section_size
        end = (i + 1) * section_size if i < 7 else 171
        expected_mean = np.mean(spectral_centroid[start:end])

        np.testing.assert_allclose(collapsed[i, 0], expected_mean, rtol=1e-5), \
            f"Collapsed section {i} does not match expected mean"

DIV_STFT_MAGS = np.abs(np.random.randn(WINDOWS, FREQUENCY_BINS, TIME_FRAMES))
DIV_STFT_MAGS /= np.max(DIV_STFT_MAGS)
DIV_STFT_VOCAL_MAG = np.abs(np.random.randn(WINDOWS, FREQUENCY_BINS, TIME_FRAMES))
DIV_STFT_VOCAL_MAG /= np.max(DIV_STFT_VOCAL_MAG)
def compute_features(featurizer): 
    return featurizer.compute_features(DIV_STFT_MAGS, DIV_STFT_VOCAL_MAG, SIGNAL, BPM)

"""computes all the features for the input song after preprocessing has been complete.
input:
    DIV_STFT_MAGS (ndarray, complex type, 3D with shape (WINDOWS, FREQUENCY_BINS, TIME_FRAMES))
    DIV_STFT_VOCAL_MAG (ndarray, non-negative values, 3D with shape (WINDOWS, FREQUENCY_BINS, TIME_FRAMES))
    SIGNAL (ndarray, floats, 1 dimensional)
    BPM (Float)
returns:
    collapsed_features, dictionary which contains:
        - collapsed_rolloff: float
        - collapsed_centroid: float
        - collapsed_bandwidth: float
        - collapsed_contrast: float
        - collapsed_rms: float, decibels range [<=0]
        - collapsed_spectral_flux: float
        - collapsed_dynamic_range: float, decibels range [<=0]
        - collapsed_instrumentalness: float, range [0-1]
        - major_key: string
        - minor_key: string
        - BPM: float, rounded"""
def test_compute_features(featurizer):
    collapsed_features = featurizer.compute_features(DIV_STFT_MAGS, DIV_STFT_VOCAL_MAG, SIGNAL, BPM) 

    """test DIV_STFT_MAGS is an ndarray """
    #check that it is an numpy array
    assert isinstance(DIV_STFT_MAGS, np.ndarray), (
        f"DIVIDED_STFT_MAG Expected numpy array of floats, got {type(DIV_STFT_MAGS)}"
        f"{getattr(DIV_STFT_MAGS, 'dtype', 'N/A')}")  #print type if not array
    #check that it is 3 dimensional:
    assert len(DIV_STFT_MAGS.shape) == 3, (
        f"divided_stft_signal_mag must be 3D, got {len(DIV_STFT_MAGS.shape)}D")
    #check that it contains magnitudes (non-negative floats for STFT magnitudes)
    assert np.issubdtype(DIV_STFT_MAGS.dtype, np.floating) and np.all(DIV_STFT_MAGS >= 0), (
        f"DIVIDED_STFT_MAG must contain non-negative floats (STFT magnitudes), "
        f"got dtype={DIV_STFT_MAGS.dtype} with min={np.min(DIV_STFT_MAGS):.2f}")
    
    """test DIV_STFT_VOCAL_MAG is an ndarray """
    #check that it is an numpy array
    assert isinstance(DIV_STFT_VOCAL_MAG, np.ndarray), (
        f"DIVIDED_STFT_MAG Expected numpy array of floats, got {type(DIV_STFT_VOCAL_MAG)}"
        f"{getattr(DIV_STFT_VOCAL_MAG, 'dtype', 'N/A')}")  #print type if not array
    #check that it is 3 dimensional:
    assert len(DIV_STFT_VOCAL_MAG.shape) == 3, (
        f"divided_stft_signal_mag must be 3D, got {len(DIV_STFT_VOCAL_MAG.shape)}D")
    #check that it contains magnitudes (non-negative floats for STFT magnitudes)
    assert np.issubdtype(DIV_STFT_VOCAL_MAG.dtype, np.floating) and np.all(DIV_STFT_VOCAL_MAG >= 0), (
        f"DIVIDED_STFT_MAG must contain non-negative floats (STFT magnitudes), "
        f"got dtype={DIV_STFT_VOCAL_MAG.dtype} with min={np.min(DIV_STFT_VOCAL_MAG):.2f}")
    
    """repurpose the signal checks (already done probably not necessary)"""
    assert isinstance(SIGNAL, np.ndarray) and np.issubdtype(SIGNAL.dtype, np.floating), (
        f"SIGNAL Expected numpy array of floats, got {type(SIGNAL)} with dtype "
        f"{getattr(SIGNAL, 'dtype', 'N/A')}")  #print type if not array
    #check for SIGNAL being flat, and therefore monochannel:
    assert len(SIGNAL.shape) == 1, (f"SIGNAL has the wrong shape, is not flat: {SIGNAL.shape}")
    assert isinstance(BPM, float), f"BPM Expected float, got {type(BPM)}" #check BPM

    """test the outputs of collapsed_features"""
    # Validate the Keys---
    expected_keys = {
        "collapsed_rolloff", 
        "collapsed_centroid", 
        "collapsed_bandwidth",
        "collapsed_contrast", 
        "collapsed_rms", 
        "collapsed_flux", 
        "collapsed_dynamic_range", 
        "collapsed_instrumentalness",
        "major_key", 
        "minor_key", 
        "bpm"}
    
    assert set(collapsed_features.keys()) == expected_keys, "Missing/extra keys"

    #Type and Range Checks for the float features---
    float_features = [
        "collapsed_rolloff", 
        "collapsed_centroid", 
        "collapsed_bandwidth",
        "collapsed_contrast", 
        "collapsed_flux"]
    for key in float_features:
        assert isinstance(collapsed_features[key], np.ndarray) and np.issubdtype(collapsed_features[key].dtype, np.floating), (
        f"Expected numpy array of floats, got {type(collapsed_features[key])} with dtype "
        f"{getattr(collapsed_features[key], 'dtype', 'N/A')}")  #print type if not array

        assert np.all(collapsed_features[key] >= 0), f"{key} = {collapsed_features[key]}, cannot be negative"

    # test for collapsed_rms, ndarray of floats, negative due to normalized signal:
    assert isinstance(collapsed_features['collapsed_rms'], np.ndarray) and np.issubdtype(collapsed_features['collapsed_rms'].dtype, np.floating), (
        f"collapsed_rms expectets ndarray of floats, got {type(collapsed_features['collapsed_rms'])} with dtype "
        f"{getattr(collapsed_features['collapsed_rms'], 'dtype', 'N/A')}")  #print type if not array
    assert np.all(collapsed_features['collapsed_rms'] <= 0), f"max of collapsed_rms = {np.max(collapsed_features['collapsed_rms'])}, all values must be ≤0 dB"

    # test for collapsed_dynamic_range, which is float, and positive, as it is max-average:
    assert isinstance(collapsed_features['collapsed_dynamic_range'], np.ndarray) and np.issubdtype(collapsed_features['collapsed_dynamic_range'].dtype, np.floating), (
        f"collapsecollapsed_dynamic_ranged_rms expectets ndarray of floats, got {type(collapsed_features['collapsed_dynamic_range'])} with dtype "
        f"{getattr(collapsed_features['collapsed_dynamic_range'], 'dtype', 'N/A')}")  #print type if not array
    assert np.all(collapsed_features['collapsed_dynamic_range'] >= 0), \
        f"max of collapsed_dynamic_range = {np.max(collapsed_features['collapsed_dynamic_range'])}, all values must be >= 0 dB"

    # Instrumentalness
    assert np.all(0 <= collapsed_features["collapsed_instrumentalness"]) and np.all(collapsed_features["collapsed_instrumentalness"] <= 1), (
        f"instrumentalness = {collapsed_features['collapsed_instrumentalness']} is not in [0,1]")

    # key and scale:
    valid_keys = {"C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab",  "A", "A#/Bb", "B"}
    valid_keys_major = {f"{key} Major" for key in valid_keys}
    valid_keys_minor = {f"{key} Minor" for key in valid_keys}
    assert collapsed_features["major_key"] in valid_keys_major, f"Major Key = {collapsed_features['major_key']}, Invalid major key"
    assert collapsed_features["minor_key"] in valid_keys_minor, f"Minor Key = {collapsed_features['minor_key']}, Invalid minor key"

    # BPM, simply check for integrity
    assert isinstance(collapsed_features["bpm"], int), f"collapsed_features[bpm] Expected int, got {type(collapsed_features['bpm'])}"
    assert collapsed_features["bpm"] > 0, f"collapsed_features[bpm] is must be > 0"

    # Spectral centroid < rolloff
    assert np.all(collapsed_features["collapsed_centroid"] < collapsed_features["collapsed_rolloff"]), (
        f"centroid = {collapsed_features['collapsed_centroid']}," 
        f"rolloff = {collapsed_features['collapsed_rolloff']}",
        "Spectral centroid should be < rolloff")