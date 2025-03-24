from flask import Flask, request, jsonify
import base64
from client import Client  # Updated Client class
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Define the backend server IP (should be a DIFFERENT computer's IP)
BACKEND_SERVER_IP = "172.20.10.2"  # Change this to the actual backend machine's IP
BACKEND_SERVER_PORT = 8000  # Ensure this matches the backend server's port

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Allow external devices to access
