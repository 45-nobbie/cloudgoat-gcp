from flask import Flask, request, jsonify

app = Flask(__name__)

FLAG = "FLAG{metadata-exfil-success}"

@app.route('/')
def index():
    return "Welcome to the vulnerable internal API. Try /api/flag."

@app.route('/api/flag')
def get_flag():
    token = request.headers.get("Authorization", "")
    if "Bearer ya29" in token or "Bearer fake" in token:
        return jsonify({"flag": FLAG})
    return jsonify({"error": "unauthorized"}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
