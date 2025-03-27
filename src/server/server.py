# server.py (replaces socket-based backend with Flask API)
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import os


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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

        # Simulated output
        recommended_ids = [
            "6rqhFgbbKwnb9MLmUQDhG6",
            "0VjIjW4GlUZAMYd2vXMi3b",
            "4iV5W9uYEdYUVa79Axb7Rh"
        ]

        return jsonify({"spotify_ids": recommended_ids})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
