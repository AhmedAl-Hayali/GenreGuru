from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import os
import subprocess
import time
import requests
import json

app = Flask(__name__)
CORS(app)

URL_STORE_ENDPOINT = "https://url-store.onrender.com/update-url"

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
    data = request.json
    is_wav_file = data.get("is_wav_file", False)

    try:
        if is_wav_file:
            base64_wav = data["file"]
            save_path = save_wav_file(base64_wav)
            if not save_path:
                return jsonify({"error": "Could not save WAV file"}), 500
        else:
            spotify_id = data["spotify_id"]
            print(f"Received Spotify ID: {spotify_id}")

        recommended_ids = [
            "6rqhFgbbKwnb9MLmUQDhG6",
            "0VjIjW4GlUZAMYd2vXMi3b",
            "4iV5W9uYEdYUVa79Axb7Rh"
        ]

        return jsonify({"spotify_ids": recommended_ids})

    except Exception as e:
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

if __name__ == "__main__":
    start_ngrok_and_post_url()
    app.run(host="0.0.0.0", port=5000)
