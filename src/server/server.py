from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import subprocess
import time
import requests
import threading

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

URL_STORE_ENDPOINT = "https://genreguru.onrender.com/update-url"

# Dummy Deezer Tracks List
deezer_tracks = [
    {
        "id": 3135556,
        "title": "Harder, Better, Faster, Stronger",
        "isrc": "GBDUW0000059",
        "duration": 226,
        "preview": "https://cdnt-preview.dzcdn.net/api/1/1/c/4/d/0/c4d7dbe3524ba59d2ad06d8cccd2484f.mp3?hdnea=exp=1743103632~acl=/api/1/1/c/4/d/0/c4d7dbe3524ba59d2ad06d8cccd2484f.mp3*~data=user_id=0,application_id=42~hmac=4de88944ce5d1788662d9a9983f9bf52411d0821c7bd5b93bc92d8e58bcd3011"
    }
]


def save_wav_file(encoded_wav, output_path="received_audio.wav"):
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
            ...
        else:
            deezer_track = data.get("deezer_track")
            print("Received Deezer Track:", deezer_track)

            if not deezer_track:
                raise ValueError("Missing deezer_track in request")

            return jsonify({"deezer_tracks": [deezer_track]})
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
