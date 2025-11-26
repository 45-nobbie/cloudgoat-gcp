from flask import Flask, jsonify, request
import os
import json
import time
from flask_cors import CORS, cross_origin
import subprocess
from flask import make_response

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
FLAGS_FILE = os.path.join(DATA_DIR, 'flags.json')
LEADERBOARD_FILE = os.path.join(DATA_DIR, 'leaderboard.json')

os.makedirs(DATA_DIR, exist_ok=True)
# Ensure files exist
if not os.path.exists(FLAGS_FILE):
    with open(FLAGS_FILE, 'w') as f:
        json.dump({
            "metadata-exfil": "FLAG{metadata-exfil-demo}",
            "gcs-key": "FLAG{gcs-key-demo}",
            "ssrf": "FLAG{ssrf-demo}",
            "iam-misconfig": "FLAG{iam-misconfig-demo}",
            "workload-identity": "FLAG{workload-identity-demo}",
            "ci-supply-chain": "FLAG{ci-supply-chain-demo}"
        }, f, indent=2)

if not os.path.exists(LEADERBOARD_FILE):
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump([], f)

def load_flags():
    with open(FLAGS_FILE, 'r') as f:
        return json.load(f)

def add_solve(user, challenge, when=None):
    when = when or int(time.time())
    with open(LEADERBOARD_FILE, 'r') as f:
        lb = json.load(f)
    lb.append({"user": user or "anon", "challenge": challenge, "time": when})
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(lb, f, indent=2)

def repo_root():
    # backend file path: <repo>/portal/backend/app.py
    # repo_root should be two levels up from this file
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def run_compose_for_challenge(challenge_id, action="up"):
    """
    Runs docker-compose -f <repo_root>/challenges/<challenge_id>/local/docker-compose.yml up -d
    Returns (ok: bool, output: str)
    """
    compose_file = os.path.join(repo_root(), "challenges", challenge_id, "local", "docker-compose.yml")
    if not os.path.exists(compose_file):
        return False, f"compose file not found at {compose_file}"
    try:
        if action == "up":
            cmd = ["docker-compose", "-f", compose_file, "up", "-d", "--build"]
        elif action == "stop":
            cmd = ["docker-compose", "-f", compose_file, "stop"]
        elif action == "down":
            cmd = ["docker-compose", "-f", compose_file, "down"]
        else:
            return False, f"unknown action {action}"
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True, proc.stdout + proc.stderr
    except subprocess.CalledProcessError as e:
        # return stdout/stderr or the exception string
        return False, (e.stdout or "") + (e.stderr or "") or str(e)
    




@app.route('/api/challenges/<cid>/deploy', methods=['OPTIONS'])
def deploy_options(cid):
    # Echo Origin or default to localhost dev origin
    origin = request.headers.get("Origin", "http://127.0.0.1:5500")
    resp = make_response("", 204)
    resp.headers['Access-Control-Allow-Origin'] = origin
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Accept'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    return resp





@app.route('/api/challenges/<cid>/deploy', methods=['POST', 'OPTIONS'])
@cross_origin(origins="http://localhost:8000",
              methods=['POST', 'OPTIONS'],
              allow_headers=['Content-Type','Authorization','X-Requested-With'],
              supports_credentials=True)
def deploy_challenge(cid):
    data = request.get_json() or {}
    action = data.get("action", "start")

    # Use your existing run_compose_for_challenge or run_compose_async function
    if action == "start":
        ok, out = run_compose_for_challenge(cid, action="up")
        if ok:
            return jsonify({"success": True, "message": f"{cid} deployed locally", "output": out}), 200
        else:
            return jsonify({"success": False, "message": f"deploy failed: {out}"}), 500

    if action == "stop":
        ok, out = run_compose_for_challenge(cid, action="stop")
        if ok:
            return jsonify({"success": True, "message": f"{cid} stopped locally", "output": out}), 200
        else:
            return jsonify({"success": False, "message": f"stop failed: {out}"}), 500

    return jsonify({"success": False, "message": "invalid action"}), 400

@app.route('/api/challenges', methods=['GET'])
def list_challenges():
    flags = load_flags()
    # metadata for UI
    meta = [
        {"id":"metadata-exfil","title":"Metadata API Secret Exfiltration","points":100,
         "summary":"Retrieve VM service account token from metadata and call internal API.","hints":[
           "Metadata server: http://169.254.169.254/",
           "Use header Metadata-Flavor: Google to query metadata"
         ]},
        {"id":"gcs-key","title":"Public GCS Service Account Key","points":100,"summary":"Find a leaked SA key in a public bucket.","hints":["Look for public buckets","Download .json key and authenticate locally"]},
        {"id":"ssrf","title":"SSRF to metadata","points":150,"summary":"Exploit SSRF to access metadata server.","hints":["Check server-side URL fetch endpoints","Try internal IPs like 169.254.169.254"]},
        {"id":"iam-misconfig","title":"Overly-permissive IAM Binding","points":150,"summary":"Find resources exposed via bad IAM policy.","hints":["Look for allUsers bindings","Use gcloud or APIs to enumerate resources"]},
        {"id":"workload-identity","title":"Workload Identity misconfig","points":200,"summary":"Impersonate service account via misconfig.","hints":["Check GKE service account mappings","Look for token exchange endpoints"]},
        {"id":"ci-supply-chain","title":"CI pipeline abuse","points":200,"summary":"Abuse insecure CI to get secrets or push artifacts.","hints":["Inspect build configs","Find writable artifact storage endpoint"]}
    ]
    return jsonify(meta)

@app.route('/api/submit-flag', methods=['POST'])
def submit_flag():
    data = request.get_json() or {}
    cid = data.get('challengeId')
    flag = data.get('flag','').strip()
    if not cid or not flag:
        return jsonify({"success": False, "message": "challengeId and flag required"}), 400
    flags = load_flags()
    expected = flags.get(cid)
    if expected and flag == expected:
        add_solve(None, cid)
        return jsonify({"success": True, "message": "Flag accepted"})
    return jsonify({"success": False, "message": "Incorrect flag"}), 200

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    with open(LEADERBOARD_FILE,'r') as f:
        lb = json.load(f)
    return jsonify(lb)


# @app.route('/api/challenges/<cid>/deploy', methods=['POST'])
# def deploy_challenge(cid):
    # data = request.get_json() or {}
    # action = data.get("action")

    # # LOCAL MODE — use docker compose
    # if action == "start":
    #     try:
    #         subprocess.run(["docker", "compose", "up", "-d", cid], check=True)
    #         return jsonify({"ok": True, "message": f"{cid} deployed (local docker)"}), 200
    #     except subprocess.CalledProcessError:
    #         return jsonify({"ok": False, "message": "docker compose failed"}), 500

    # if action == "stop":
    #     try:
    #         subprocess.run(["docker", "compose", "stop", cid], check=True)
    #         return jsonify({"ok": True, "message": f"{cid} stopped"}), 200
    #     except subprocess.CalledProcessError:
    #         return jsonify({"ok": False, "message": "docker compose failed"}), 500

    # return jsonify({"ok": False, "message": "invalid action"}), 400




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',4000)), debug=True)


CORS(app,
     resources={r"/api/*": {"origins": ["http://localhost:8000", "http://127.0.0.1:5500"]}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"])