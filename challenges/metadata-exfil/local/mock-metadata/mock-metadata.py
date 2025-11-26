#!/usr/bin/env python3
from flask import Flask, jsonify
import os

app = Flask(__name__)
ACCESS_TOKEN = os.environ.get("MOCK_TOKEN", "fake-token-12345")

@app.route("/computeMetadata/v1/instance/service-accounts/default/token")
def token():
    return jsonify({
        "access_token": ACCESS_TOKEN,
        "expires_in": 3599,
        "token_type": "Bearer"
    })

@app.route("/")
def root():
    return "Mock metadata service. Token: " + ACCESS_TOKEN

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
