from flask import Flask, request, jsonify
from flask_cors import CORS  # <-- Add this import
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # <-- Allow all origins (or restrict to localhost if you prefer)

latest_url = None

@app.route("/update-url", methods=["POST"])
def update_url():
    global latest_url
    latest_url = request.json.get("url")
    return jsonify({"status": "updated", "url": latest_url})

@app.route("/get-url", methods=["GET"])
def get_url():
    return jsonify({"url": latest_url})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)