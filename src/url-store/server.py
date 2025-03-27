from flask import Flask, request, jsonify

app = Flask(__name__)
latest_url = None

@app.route("/update-url", methods=["POST"])
def update_url():
    global latest_url
    latest_url = request.json.get("url")
    return jsonify({"status": "updated", "url": latest_url})

@app.route("/get-url", methods=["GET"])
def get_url():
    return jsonify({"url": latest_url})
