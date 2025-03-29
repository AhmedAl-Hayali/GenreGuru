import os
import warnings

#nuke all the warnings 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')
import tensorflow as tf
tf.get_logger().setLevel('ERROR')

from spleeter.separator import Separator
import soundfile as sf 
import numpy as np

class Audio_Splitter:
    """audio splitter class for instrumentalness feature. can also be used for 
    other vocal features down the line. Uses spleeter's pre-trained models"""

    def __init__(self):
        # tf.compat.v1.reset_default_graph()
        self.separator = Separator('spleeter:2stems')
        pass #no instance variables applicable
        
    """split the input waveform"""
    def split_audio(self, signal):
        """uses spleeter to separate the vocal waveform from the non-vocal waveform. 
        args:
            signal (ndarray): audio time series of the audio
        output:
            vocal_signal (ndarray): isolated vocal elements of the audio
            non_vocal_signal (ndarray): non vocal elements of the audio"""
        
        #first reshape the input signal, as it is mono. convert to stereo
        signal = signal.reshape(-1, 1)

        #apply spleeter
        # result = separator.separate(signal)
        result = self.separator.separate(signal)

        #now reconstruct our waveforms and flatten them.
        vocal_signal = result['vocals'].mean(axis=1) 
        non_vocal_signal = result['accompaniment'].mean(axis=1)
        # print(f"vocal_signal shape is: {vocal_signal.shape}")
        # print(f"non_vocal_signal shape is: {non_vocal_signal.shape}")

        #clear shesh???
        # tf.keras.backend.clear_session()
        return vocal_signal, non_vocal_signal