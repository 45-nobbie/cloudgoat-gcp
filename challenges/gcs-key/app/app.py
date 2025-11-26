#!/usr/bin/env python3
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "FLAG{gcs-key-local}")
EXPECTED_TOKEN = os.environ.get("EXPECTED_TOKEN", "gcs-token-abc123")

@app.route('/')
def index():
    return "GCS Key challenge: find leaked key in public bucket and use it to fetch /api/flag"

@app.route('/api/flag')
def flag():
    auth = request.headers.get('Authorization','')
    if auth.startswith("Bearer "):
        token = auth.split(None,1)[1]
        if token == EXPECTED_TOKEN:
            return jsonify({"flag": FLAG})
    return jsonify({"error": "unauthorized"}), 403

# small helper to mimic a vulnerable endpoint that prints hints (optional)
@app.route('/info')
def info():
    return ("Hint: check public GCS buckets. Try visiting http://localhost:5000/public-bucket/leaked-key.json")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)