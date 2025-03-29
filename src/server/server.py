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


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

URL_STORE_ENDPOINT = "https://genreguru.onrender.com/update-url"


def save_wav_file(encoded_wav, output_path=f"received_{uuid.uuid4().hex}.wav"):
    try:
        wav_data = base64.b64decode(encoded_wav)
        with open(output_path, "wb") as wav_file:
            wav_file.write(wav_data)
        print(f"WAV file saved successfully: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error saving WAV file: {e}")
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

            # This is a stub for future model predictions
            print(f"Saved WAV to: {file_path}")

            return jsonify({
                "deezer_tracks": [
                    {
                        "id": 3135556,
                        "title": "Harder, Better, Faster, Stronger",
                        "isrc": "GBDUW0000059",
                        "preview": "https://cdnt-preview.dzcdn.net/api/1/1/c/4/d/0/c4d7dbe3524ba59d2ad06d8cccd2484f.mp3?hdnea=exp=1743103749~acl=/api/1/1/c/4/d/0/c4d7dbe3524ba59d2ad06d8cccd2484f.mp3*~data=user_id=0,application_id=42~hmac=832b8683abc56db185864bb3bb98f8d588b3cef57aae3f218666243055c985dd"
                    },
                    {
                        "id": 2582901922,
                        "title": "Happier (feat. Clementine Douglas)",
                        "isrc": "GBAHT2301515",
                        "preview": "https://cdnt-preview.dzcdn.net/api/1/1/4/d/6/0/4d6b38a80a40ee56ab31dd0842c1a5eb.mp3?hdnea=exp=1743192301~acl=/api/1/1/4/d/6/0/4d6b38a80a40ee56ab31dd0842c1a5eb.mp3*~data=user_id=0,application_id=42~hmac=bc455d28bcadcdd68e33e47a4d8eb769681c76a2d78ac6eebe5b18d75ec9e858"
                    }
                ]
            })
        
        else:
            deezer_track = data.get("deezer_track")
            print("Received Deezer Track:", deezer_track)

            if not deezer_track: raise ValueError("Missing deezer_track in request")

            dz = Client()
            preview_url = dz.get_track(deezer_track["id"]).preview
            response = requests.get(preview_url)
            mp3_bytes = BytesIO(response.content)

            print("successfully gotten the response")
            # Step 2: Convert MP3 to WAV using pydub
            audio = AudioSegment.from_file(mp3_bytes, format="mp3")
            wav_object = BytesIO()
            audio.export(wav_object, format="wav")
            wav_object.seek(0)


            # with open("preview.wav", "wb") as f: f.write(wav_object.read())

            # print("WAV file saved as preview.wav")
            # print(data.shape)


            return jsonify({
                "deezer_tracks": [
                    {
                        "id": 3135556,
                        "title": "Harder, Better, Faster, Stronger",
                        "isrc": "GBDUW0000059",
                        "preview": "https://cdnt-preview.dzcdn.net/api/1/1/c/4/d/0/c4d7dbe3524ba59d2ad06d8cccd2484f.mp3?hdnea=exp=1743103749~acl=/api/1/1/c/4/d/0/c4d7dbe3524ba59d2ad06d8cccd2484f.mp3*~data=user_id=0,application_id=42~hmac=832b8683abc56db185864bb3bb98f8d588b3cef57aae3f218666243055c985dd"
                    },
                    {
                        "id": 2582901922,
                        "title": "Happier (feat. Clementine Douglas)",
                        "isrc": "GBAHT2301515",
                        "preview": "https://cdnt-preview.dzcdn.net/api/1/1/4/d/6/0/4d6b38a80a40ee56ab31dd0842c1a5eb.mp3?hdnea=exp=1743192301~acl=/api/1/1/4/d/6/0/4d6b38a80a40ee56ab31dd0842c1a5eb.mp3*~data=user_id=0,application_id=42~hmac=bc455d28bcadcdd68e33e47a4d8eb769681c76a2d78ac6eebe5b18d75ec9e858"
                    }
                ]
            })

    except Exception as e:
        print("Error in /process:", str(e))
        return jsonify({"error": str(e)}), 500

    
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "Backend is alive!"}), 200

def start_ngrok_and_post_url():
    # Start ngrok in background
    subprocess.Popen(["ngrok", "http", "5000"])
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
