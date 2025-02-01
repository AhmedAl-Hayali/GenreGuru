import librosa

"""Temporary BPM compute"""
def compute_bpm(signal, target_sample_rate):
    """temporary BPM calculation is simply done as librosa.feature.bpm. 
    this is because @baleanu code has not been updated to same branch, 
    and testing of the window division based on BPM relies on this module
    this is to be replaced with the real computeBPM function, already implementedby @baleanu"""
    bpm = librosa.feature.tempo(y=signal, sr=target_sample_rate)
    return bpm[0]