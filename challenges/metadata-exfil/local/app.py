#!/usr/bin/env python3
# Local variant of the metadata-exfil challenge app.
# Uses METADATA_URL env var to fetch token (so a mock metadata server can be injected for local testing).

from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Flag used for this challenge. In production this would come from Secret Manager.
FLAG = os.environ.get("CHALLENGE_FLAG", "FLAG{metadata-exfil-local}")

# Metadata endpoint URL (defaults to real GCP endpoint)
METADATA_URL = os.environ.get(
    "METADATA_URL",
    "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token"
)
METADATA_HEADERS = {"Metadata-Flavor": "Google"}

@app.route('/')
def index():
    return "Internal API: Try /api/flag"

@app.route('/api/flag')
def flag():
    auth = request.headers.get('Authorization','')
    try:
        r = requests.get(METADATA_URL, headers=METADATA_HEADERS, timeout=3)
        r.raise_for_status()
        meta = r.json()
        current_token = meta.get('access_token','')
    except Exception as e:
        return jsonify({"error":"metadata lookup failed", "detail": str(e)}), 500

    if auth.startswith("Bearer "):
        provided = auth.split(None,1)[1]
        if provided == current_token:
            return jsonify({"flag": FLAG})
    return jsonify({"error":"unauthorized"}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
