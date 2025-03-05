"""
Computes instrumentalness [0~1] where a lower value means more vocals and a higher value means less vocals.
Instrumentalness is being defined as:
Instrumentalness = 1 - (vocal_energy / original_energy)
Somewhat attempts to account for spleeter's imperfect isolation (further exacerbated by using mono input).
Assumption: All inputs have the same shape. BPM will not be recomputed, so should have the same size.

tests for instrumentalness:
Parameters:
    original_rms (ndarray): Audio time series of original signal
    - check for numpy array of floats
    - check for valid RMS values range
    vocal_rms (ndarray): audio time series of isolated vocals
    - check for numpy array of floats
    - check for valid RMS values range
Returns:
    instrumentalness (ndarray): Instrumentalness value at each window.
    - check for numpy array of floats
    - check for valid values range
    mean_instrumentalness (float): Overall instrumentalness of the entire song.
    - check for float type
"""

def test_instrumentalness(original_rms, vocal_rms):

    """"""
