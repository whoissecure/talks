from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)
SECRET = "supersecret"

@app.route("/internal", methods=["POST"])
def internal():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid JSON"}), 400

    token = jwt.encode({
        "user": data.get("user", ""),
        "role": data.get("role", "")
    }, SECRET, algorithm="HS256")

    return jsonify({"token": token}), 200

@app.route("/verify", methods=["POST"])
def verify():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid JSON"}), 400

    token = data.get("token")
    if not token:
        return jsonify({"error": "Token missing"}), 400

    try:
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
        return jsonify({"valid": True, "payload": decoded}), 200
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
