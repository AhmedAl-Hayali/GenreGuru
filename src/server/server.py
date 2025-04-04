from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import subprocess
import time
import requests
import threading
import uuid
from io import BytesIO
from pydub import AudioSegment
from deezer import Client
from src.featurizer.main_featurizer import Featurizer
from src.recommendation.recommend import Recommendation
from src.db.db_functions import DB_Engine
import pandas as pd

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
URL_STORE_ENDPOINT = "https://genreguru.onrender.com/update-url"

def save_wav_file(wav_file, output_dir='.', custom_name=None):
    try:
        filename = custom_name or f'received_{uuid.uuid4().hex}.wav'
        output_path = f'{output_dir}/{filename}'

        with open(output_path, 'wbn') as f:
            f.write(wav_file.read())

        print(f'WAV file saved successfully: {output_path}')
        return output_path
    except Exception as e:
        print(f'Error saving WAV file: {e}')
        return None

@app.route("/process", methods=["POST"])
def process_request():
    try:
        data = request.json
        print("Received JSON data:", data)

        is_wav_file = data.get("is_wav_file", False)

        if is_wav_file:
            encoded_wav = data.get("file")
            if not encoded_wav:
                raise ValueError("Missing encoded WAV file")

            file_path = save_wav_file(encoded_wav)
            if not file_path:
                raise ValueError("Failed to save WAV file")

            # directly obtain our dataframe here
            print(f"Saved WAV to: {file_path}")
            db = DB_Engine()
            featurizer = Featurizer()

            #obtain features for the user uploaded wav file
            features = featurizer.run(file_path)
            print("wav file featurized")

            feat_names = ['spctrl_rlf',
                          'spctrl_cntrd',
                          'spctrl_bw',
                          'spctrl_cntrst',
                          'rms',
                          'spctrl_flux',
                          'dnmc_rng',
                          'instrmntlns']

            features = [feature.flatten() for feature in features.values()]
            print(features)
            #instead of using deezer_id (we dont have one insert a fake id and the associated features:)
            spoofed_id = "00000000"
            DB_dataframe = db.obtain_all_records()
            print("obtained database dataframe")

            #insert spoofed_id, features into db_dataframe
            x = pd.DataFrame([spoofed_id] + features, columns=['track_id']+[f'{feat_name}_{i}' for feat_name in feat_names for i in range(1, 8+1)]+['bpm', 'keymjr', 'keymnr'])
            DB_dataframe = pd.concat([DB_dataframe, x])

            print("obtained database dataframe")
            recommender = Recommendation(data=DB_dataframe)
            recommended_songs = recommender.get_similar_songs(spoofed_id)
            print("recommendations generated")

            print(recommended_songs.index.to_numpy())
            recommended_songs_ids = recommended_songs.index.to_numpy()
            print("extracted ids")
            recommended_songs_ids = [int(sid) for sid in recommended_songs_ids]
            print('yo wassup', recommended_songs_ids)

            return jsonify({"track_ids": recommended_songs_ids})
        
        else:
            deezer_track = data.get("deezer_track")
            print("Received Deezer Track:", deezer_track)

            if not deezer_track: raise ValueError("Missing deezer_track in request")
            featurizer = Featurizer()
            dz = Client()
            db = DB_Engine()

            
            deezer_ID = str(deezer_track["id"])
            print('deezer id:', deezer_ID)
            print("successfully gotten the deezer ID")
            # in the case where the db is already there:
            if not db.check_if_record_exists(deezer_ID):
                print("successfully gotten the deezer ID NOT FOUND! FEATURIZE")
                #fetch preview
                preview_url = dz.get_track(deezer_ID).preview
                response = requests.get(preview_url)
                mp3_bytes = BytesIO(response.content)

                print("Successfully extracted preview url content")
                # Step 2: Convert MP3 to WAV using pydub
                audio = AudioSegment.from_file(mp3_bytes, format="mp3")
                wav_object = BytesIO()
                audio.export(wav_object, format="wav")
                wav_object.seek(0)
                print("Successfully exported to wav")

                features = featurizer.run(wav_object)
                print("Successfully computed features")

                #now insert our record
                db.insert_record(deezer_ID, features)
                print("Successfully inserted record")
            
            DB_dataframe = db.obtain_all_records()
            print("obtained database dataframe")
            recommender = Recommendation(data=DB_dataframe)

            recommended_songs = recommender.get_similar_songs(deezer_ID)
            print("recommendations generated")
            print(recommended_songs.index.to_numpy())
            recommended_songs_ids = recommended_songs.index.to_numpy()
            print("extracted ids")
            recommended_songs_ids = [int(sid) for sid in recommended_songs_ids]

            return jsonify({"track_ids": recommended_songs_ids})
            

    except Exception as e:
        print("Error in /process:", str(e))
        return jsonify({"error": str(e)}), 500

    
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "Backend is alive!"}), 200

def start_ngrok_and_post_url():
    subprocess.Popen(["./ngrok.exe", "http", "5000"])
    print("Started ngrok... waiting for public URL")

    # Give ngrok time to initialize
    time.sleep(5)

    try:
        # Fetch public ngrok URL
        tunnels_info = requests.get("http://127.0.0.1:4040/api/tunnels").json()
        public_url = tunnels_info["tunnels"][0]["public_url"]
        print(f"Ngrok URL: {public_url}")

        # Send to URL store
        payload = {"url": public_url}
        res = requests.post(URL_STORE_ENDPOINT, json=payload)
        if res.status_code == 200:
            print("Ngrok URL shared with frontend successfully.")
        else:
            print("Failed to update Render URL store.")

    except Exception as e:
        print(f"Error setting up ngrok tunnel: {e}")

def periodically_update_ngrok_url(interval=60):
    def updater():
        while True:
            try:
                tunnels_info = requests.get("http://127.0.0.1:4040/api/tunnels").json()
                public_url = tunnels_info["tunnels"][0]["public_url"]
                print(f"[Auto-Update] Current Ngrok URL: {public_url}")

                payload = {"url": public_url}
                res = requests.post(URL_STORE_ENDPOINT, json=payload)
                if res.status_code == 200:
                    print("[Auto-Update] Ngrok URL updated successfully.")
                else:
                    print(f"[Auto-Update] Failed to update URL. Status: {res.status_code}")
            except Exception as e:
                print(f"[Auto-Update] Error updating Ngrok URL: {e}")

            time.sleep(interval)

    thread = threading.Thread(target=updater, daemon=True)
    thread.start()


if __name__ == "__main__":
    start_ngrok_and_post_url()
    periodically_update_ngrok_url(interval=60) # updates every 60 seconds
    app.run(host="0.0.0.0", port=5000)
