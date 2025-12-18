from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

DATA_FILE = "results.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json

    if not data:
        return jsonify({"status": "error"}), 400

    data["server_time"] = datetime.utcnow().isoformat()

    all_data = load_data()
    all_data.append(data)
    save_data(all_data)

    print("Received:", data)
    return jsonify({"status": "ok"})

@app.route("/")
def home():
    return "Server is running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
