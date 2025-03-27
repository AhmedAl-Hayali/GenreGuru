from flask import Flask, request, jsonify
import base64
from client import Client  # Updated Client class
from flask_cors import CORS
import configparser
import requests

# Initialize Flask app
app = Flask(__name__)
CORS(app)

cfg = configparser.ConfigParser()
cfg.read('src/client/genre-guru/.env.local.toml')

# Define the backend server IP (should be a DIFFERENT computer's IP)
BACKEND_SERVER_IP = cfg['server']['server_ip']  # Change this to the actual backend machine's IP
BACKEND_SERVER_PORT = cfg['server']['server_port']  # Ensure this matches the backend server's port

SPOTIFY_CLIENT_ID = cfg['spotify']['client_id']
SPOTIFY_CLIENT_SECRET = cfg['spotify']['client_secret']

def send_to_backend(message):
    """
    Establishes a connection with the backend server and sends a message.
    """
    client = Client(BACKEND_SERVER_IP, BACKEND_SERVER_PORT)

    if not client.connect():
        return {"error": "Failed to connect to backend"}

    response = client.send_message(message)
    client.close()

    if response:
        return response.split(",")  # Assuming backend sends a comma-separated list of Spotify IDs
    else:
        return {"error": "No response from backend"}

@app.route("/process", methods=["POST"])
def process_request():
    """
    Handles requests from the React frontend and forwards them to the backend server.
    """
    try:
        data = request.json
        is_wav_file = data.get("is_wav_file", False)

        if is_wav_file:
            base64_wav = data["file"]
            response = send_to_backend(f"WAV_FILE:{base64_wav}")
        else:
            spotify_id = data["spotify_id"]
            response = send_to_backend(f"SPOTIFY_ID:{spotify_id}")

        return jsonify({"spotify_ids": response})

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/get_spotify_token", methods=["GET"])
def get_spotify_token():
    try:
        auth_header = base64.b64encode(
            f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode("utf-8")
        ).decode("utf-8")

        response = requests.post(
            "https://accounts.spotify.com/api/token",
            data={"grant_type": "client_credentials"},
            headers={
                "Authorization": f"Basic {auth_header}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )

        if response.status_code == 200:
            access_token = response.json().get("access_token")
            return jsonify({"access_token": access_token})
        else:
            print("Spotify auth error:", response.text)
            return jsonify({"error": "Spotify auth failed", "details": response.text}), 400

    except Exception as e:
        print("Exception during Spotify auth:", e)
        return jsonify({"error": str(e)}), 500
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Allow external devices to access
