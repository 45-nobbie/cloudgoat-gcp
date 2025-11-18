#!/bin/bash
set -euo pipefail

# Install python and pip
apt-get update
apt-get install -y python3 python3-venv python3-pip curl

# Create app dir
APP_DIR="/opt/metadata-exfil-app"
mkdir -p "$APP_DIR"
cd "$APP_DIR"

# Write app.py
cat > app.py <<'PY'
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Flag injected by Terraform via startup script templating
FLAG = "${flag_value}"

@app.route('/')
def index():
    return "Internal API: Try /api/flag"

@app.route('/api/flag')
def flag():
    auth = request.headers.get('Authorization','')
    # fetch current metadata token
    try:
        meta = requests.get(
            "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token",
            headers={"Metadata-Flavor":"Google"},
            timeout=2
        ).json()
        current_token = meta.get('access_token','')
    except Exception as e:
        return jsonify({"error":"metadata lookup failed", "detail": str(e)}), 500

    if auth.startswith("Bearer "):
        provided = auth.split(None,1)[1]
        if provided == current_token:
            return jsonify({"flag": FLAG})
    return jsonify({"error":"unauthorized"}), 403

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
PY

# Write requirements
cat > requirements.txt <<'REQ'
Flask==2.2.5
requests==2.31.0
REQ

# Create systemd service
cat > /etc/systemd/system/metadata-exfil.service <<'SVC'
[Unit]
Description=Metadata Exfil Challenge Service
After=network.target

[Service]
WorkingDirectory=/opt/metadata-exfil-app
ExecStart=/usr/bin/python3 /opt/metadata-exfil-app/app.py
Restart=always
User=root

[Install]
WantedBy=multi-user.target
SVC

# Start the service
systemctl daemon-reload
systemctl enable metadata-exfil.service
systemctl start metadata-exfil.service

# Done
echo "Metadata exfil app deployed. Flag is present in the app but only returned when valid token used."
