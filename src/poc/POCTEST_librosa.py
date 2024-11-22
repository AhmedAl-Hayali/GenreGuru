import os
import numpy as np
import librosa
from pydub import AudioSegment

def mp3_to_wav(mp3_path, wav_path):
    """Convert an MP3 file to WAV using pydub."""
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")

def librosa_beat_track_test(audio_file_path):
    wav_path = "temp_audio.wav"
    mp3_to_wav(audio_file_path, wav_path)
    audio_file = librosa.load(wav_path, sr=None, mono=True)
    y, sr = audio_file
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    print(tempo)
    # print('Estimated tempo: {:.2f} beats per minute'.format(tempo))
    # beat_times = librosa.frames_to_time(beat_frames, sr=sr)

#dynamic programming implementation of beat tracking - converted code from 
# https://www.tandfonline.com/doi/epdf/10.1080/09298210701653344?needAccess=true
def dynamic_prog_beats(localscore, period, alpha):
    #localscore = onset strength envelope 
    #period = target tempo period in samples
    #alpha = weight applied to transition cost
    #based algorithm (dynamic programming method) provided by Daniel P. W. Ellis
    backlink =  -np.ones(len(localscore))
    cumulative_score = localscore

    #search range for previous beat
    prange = np.arange(round(-2 * period), -round(period / 2) - 1, -1)

    #compute log window over range
    tx_cost = (-alpha*abs(np.square(np.log10(prange/period))))
    
    for i in range(max(-prange +  1), len(localscore)):
        time_range = i + prange

        #search over all past iterations or some shit idfk what i mdoing bro
        scores = tx_cost + cumulative_score[time_range]

        [vv, xx] = max[scores]

        #some dp shit about adding local scores
        cumulative_score[i] = vv+localscore[i]
        #store the backtrace
        backlink[i] = time_range[xx]
    
    #start backtrace from best score
    [vv, beats] = max(cumulative_score)
    while backlink[beats[1]]>0 : beats=[backlink[beats[1]],beats]
        
audio_file_path = "src\poc\mp3s\entrance_au5.mp3"
librosa_beat_track_test(audio_file_path)