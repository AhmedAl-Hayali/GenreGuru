import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
# Set up Spotify API credentials

#extract config from json file
with open("src\poc\spotify_config.json") as f: conf = json.load(f)
c_id = conf["SPOTIFY_CLIENT_ID"]; c_secret = conf["SPOTIFY_CLIENT_SECRET"]
auth_manager = SpotifyClientCredentials(client_id=c_id, client_secret=c_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_song_name(track_id):
    #fetch ALL INFO. 
    info = sp.track(track_id)
    return info["name"]

def get_song_tempo(track_id):
    # Fetch audio features for the given track
    features = sp.audio_features(track_id)
    print(f"Song Track ID: {track_id}"); print(f"Song Name: {get_song_name(track_id)}")
    # print(f"ALL F EATURES: {features}")
    if features and features[0]: return features[0].get("tempo", "Tempo not found")
    return 'Invalid track ID or no features available'

# test
# test_id = "5oi8dkse5YTnTSWm3XgMET" #"remember me", "D4VD, arcane, league of legends"
# print(f"Tempo: {get_song_tempo(test_id)} BPM")
