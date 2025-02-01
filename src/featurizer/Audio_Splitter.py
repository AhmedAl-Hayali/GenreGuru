from spleeter.separator import Separator

"""uses spleeter to isolate the vocals and non-vocal signals in order to create instrumentalness and vocal gender features"""
def separate_signal(audio_signal):
    separator = Separator('spleeter:2stems')
    isolated_signals = separator.separate(audio_signal)
    return isolated_signals
