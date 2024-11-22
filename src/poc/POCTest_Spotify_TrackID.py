import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from POCTest_Spotify_BPM import *
# Set up Spotify API credentials

#extract config from json file
with open("src\poc\spotify_config.json") as f: conf = json.load(f)
c_id = conf["SPOTIFY_CLIENT_ID"]; c_secret = conf["SPOTIFY_CLIENT_SECRET"]
auth_manager = SpotifyClientCredentials(client_id=c_id, client_secret=c_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_track_id(song_name):
    r = sp.search(q = song_name, type = "track", limit = 1)
    track = r.get("tracks", {}).get("items", [])
    if track: return track[0]['id']
    return f"Did not find {song_name}"

#test
while True: 
    print("\n Input your song in one line, enter qqq to quit: ")
    test_var = str(input())
    if test_var == "qqq": exit()
    test_id = get_track_id(test_var)
    print(f"TEMPO: {get_song_tempo(test_id)}")
    print(f"Track ID: {test_id}")
    print(f"sanity check using get_song_name: {get_song_name(test_id)}")