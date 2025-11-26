#!/usr/bin/env python3
from flask import Flask, jsonify, send_file
import os
import json

app = Flask(__name__)

# Leaked key contains token that victim would use to access protected resource.
LEAKED_KEY = {
  "type": "service_account",
  "project_id": "demo-project",
  "client_email": "leaked@demo.iam.gserviceaccount.com",
  "token": "gcs-token-abc123"
}

@app.route('/')
def root():
    return "Mock GCS - public buckets (leaked keys)"

@app.route('/public-bucket/leaked-key.json')
def leaked_key():
    return jsonify(LEAKED_KEY)

# A real GCS would host objects; we also provide a public listing fallback
@app.route('/public-bucket/flag.txt')
def public_flag():
    return "This one is private. Get the proper credentials."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

