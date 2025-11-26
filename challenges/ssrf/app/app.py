#!/usr/bin/env python3
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
FLAG = os.environ.get("CHALLENGE_FLAG", "FLAG{ssrf-local}")

@app.route('/')
def index():
    return (
        "SSRF challenge: use /fetch?url=<url> to cause the server to request your URL. "
        "Goal: fetch internal metadata and extract token, then use it with /api/flag"
    )

# Vulnerable server-side fetch endpoint (intentionally insecure)
@app.route('/fetch')
def fetch():
    url = request.args.get('url', '').strip()
    if not url:
        return "Usage: /fetch?url=http://example", 400
    try:
        # Note: intentionally no validation or allowlists
        resp = requests.get(url, timeout=4)
        # return response text to the attacker (so they can read metadata output)
        return resp.text, resp.status_code
    except Exception as e:
        return jsonify({"error": "fetch failed", "detail": str(e)}), 500

# Flag endpoint requires a Bearer token equal to the mock metadata token
@app.route('/api/flag')
def flag():
    auth = request.headers.get('Authorization', '')
    if auth.startswith("Bearer "):
        token = auth.split(None, 1)[1]
        # token expected to match mock metadata's access_token
        if token == "meta-token-xyz":
            return jsonify({"flag": FLAG})
    return jsonify({"error": "unauthorized"}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
