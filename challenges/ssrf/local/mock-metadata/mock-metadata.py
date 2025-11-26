#!/usr/bin/env python3
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/computeMetadata/v1/instance/service-accounts/default/token')
def token():
    return jsonify({
        "access_token": "meta-token-xyz",
        "expires_in": 3599,
        "token_type": "Bearer"
    })

@app.route('/')
def root():
    return "Mock metadata for SSRF (token: meta-token-xyz)"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)
