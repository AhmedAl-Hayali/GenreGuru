import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

latest_url = None

@app.route("/update-url", methods=["POST"])
def update_url():
    global latest_url
    latest_url = request.json.get("url")
    return jsonify({"status": "updated", "url": latest_url})

@app.route("/get-url", methods=["GET"])
def get_url():
    return jsonify({"url": latest_url})

# Proxy Deezer API through Render
@app.route("/proxy/deezer", methods=["GET"])
def proxy_deezer():
    isrc = request.args.get("isrc")
    if not isrc:
        return jsonify({"error": "Missing ISRC"}), 400

    deezer_url = f"https://api.deezer.com/track/isrc:{isrc}"
    try:
        headers = {"User-Agent": "GenreGuru/1.0"}
        response = requests.get(deezer_url, headers=headers, timeout=10)
        response.raise_for_status()

        if "application/json" not in response.headers.get("Content-Type", ""):
            print("Deezer returned non-JSON content")
            return jsonify({"error": "Invalid response from Deezer"}), 502

        return jsonify(response.json())

    except requests.RequestException as e:
        print(f"Deezer proxy failed: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
