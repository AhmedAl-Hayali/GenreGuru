import numpy as np

"""module for the computation of the instrumentalness of the song.
we do so by comparing the rms of the vocals to original, in order to avoid 
extra computation on the non-vocal output. 
"""

def compute_instrumentalness(original_rms, vocal_rms, espilon = 1e-10):
    """
    computes instrumentalness [0~1] where a lower value means more vocals and a higher value means less vocals. 
    instrumentalness is being defined as such:
    Instrumentalness = 1 - (vocal_energy / original_energy)

    somewhat attempts to account for spleeter's imperfect isolation (further exaberated by using mono input). 
    assumption: all inputs have the same shape. BPM will not be recomputed, so should have same size
    args:
        original_rms (ndarray): feature vector of rms of original rms
        vocal_rms (ndarray) : feature vector of rms of the vocal portion
        espilon (float): prevents inf
    returns: 
        instrumentalness (2D ndarray): ndarray of instrumentalness value at each window
        mean_instrumentalness (float64): returns the overall instrumentalness of the entire song
    """
    instrumentalness = np.zeros((original_rms.shape[0], 1))
    mean_instrumentalness = 0

    for i in range(original_rms.shape[0]):
        #compute db difference first.
        db_diff = vocal_rms[i] - original_rms[i]

        #compute the ratio, use epsilon to avoid negative values:
        energy_ratio = 10**(db_diff / 10)
        current_instrumentalness = 1 - min(energy_ratio, 1-espilon)
        instrumentalness[i] = current_instrumentalness
        mean_instrumentalness += current_instrumentalness
        
    mean_instrumentalness /= original_rms.shape[0]
    return instrumentalness, mean_instrumentalness
