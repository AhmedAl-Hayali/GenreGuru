import os
import warnings

#nuke all the warnings 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')
import tensorflow as tf
tf.get_logger().setLevel('ERROR')

from spleeter.separator import Separator
import librosa
import soundfile as sf 
import numpy as np

from Main_Featurizer import *

"""uses spleeter to isolate the vocals and non-vocal signals in order to create instrumentalness and vocal gender features"""
def separate_vocals(input_path, output_path):
    """separates vocals from the audio track using spleeter's pretained models
    args:
        input_path (str): path to the audio input
        output_path (str): path to the audio output"""

    #create output directory if it does not exist
    os.makedirs(output_path, exist_ok = True)

    #yank file name for my own sanity
    file_name = input_path.split("/")[2].split(".")[0]
    
    #use spleeter 2-stem separator
    separator = Separator('spleeter:2stems')
    
    #load audio using librosa. 44.1khz works best for spleeter, spleeter also needs mono audio
    # signal, sample_rate = librosa.load(input_path,
    #     sr=44100,  # Required for Spleeter models
    #     mono=False  # Preserve stereo if available
    # )

    signal, sample_rate = librosa.load(input_path, sr=44100)

    #normalize amplitude
    signal = signal / np.max(np.abs(signal))

    #ensure proper shapes for spleeter to function. Reshape the audio to stereo
    signal = signal.reshape(-1, 1) #reshape necesssary because of mono input

    #perform separation. This returns a dictionary containing the data for the two signals
    result = separator.separate(signal)

    """testing if the audio splitting works well through just listening to it"""
    for stem, data in result.items():
        out = os.path.join(output_path, f"{file_name}_{stem}.wav")
        sf.write(out, data, sample_rate)
        print(f"Saved {stem} to: {out}")

# def output_audio(results, output_path = "src/split_output/"):
#     for stem, data in result.items():
#     out = os.path.join(output_path, f"{file_name}_{stem}.wav")
#     sf.write(out, data, sample_rate)
#     print(f"Saved {stem} to: {out}")


"""splitting function but this time, we accept the signal directly instead."""
def separate_audio(signal):
    """uses spleeter to separate the vocal waveform from the non-vocal waveform. 
    args:
        signal (ndarray): audio time series of the audio
    output:
        vocal_signal (ndarray): isolated vocal elements of the audio
        non_vocal_signal (ndarray): non vocal elements of the audio"""
    
    #first reshape the input signal, as it is mono. convert to stereo
    signal = signal.reshape(-1, 1)

    #apply spleeter
    separator = Separator('spleeter:2stems')
    result = separator.separate(signal)

    #now reconstruct our waveforms and flatten them.
    vocal_signal = result['vocals'].mean(axis=1) 
    non_vocal_signal = result['accompaniment'].mean(axis=1)
    # print(f"vocal_signal shape is: {vocal_signal.shape}")
    # print(f"non_vocal_signal shape is: {non_vocal_signal.shape}")
    return vocal_signal, non_vocal_signal

"""test splitting"""
def main():
    input = "src/audio/Time.wav"
    output = "src/split_output/"
    separate_vocals(input, output)

    # signal, stft_signal, sr = process_audio(input, 44100)
    # print(f"original signal shape is: {signal.shape}")
    # separate_audio(signal)


if __name__=="__main__": main()