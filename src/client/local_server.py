from flask import Flask, request, jsonify
import base64
from client import Client  # Import the Client class from client.py

# Initialize Flask app
app = Flask(__name__)

# Configure the backend server connection
BACKEND_SERVER_IP = "0.0.0.0"  # Change this to the actual backend server IP
BACKEND_SERVER_PORT = 8000  # Make sure this matches the backend server port


def send_to_backend(message):
    """
    Function to send data to the backend server via Client class.
    Handles connection, sending, and receiving data.
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
    Handles requests from the React frontend.
    - If the request contains a WAV file, it sends the Base64-encoded file to the backend.
    - If the request contains a Spotify ID, it sends the ID to the backend.
    """
    try:
        data = request.json
        is_wav_file = data.get("is_wav_file", False)

        if is_wav_file:
            # Forward the base64 string to the backend without decoding
            base64_wav = data["file"]
            response = send_to_backend(f"WAV_FILE:{base64_wav}")
        else:
            spotify_id = data["spotify_id"]
            response = send_to_backend(f"SPOTIFY_ID:{spotify_id}")  # Send Spotify ID directly

        return jsonify({"spotify_ids": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
