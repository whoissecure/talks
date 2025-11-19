from flask import Flask, request, jsonify

app = Flask(__name__)

# dirty db simulation
wallets = {"daniel":30, "miquel":30, "rooted":30}

PRODUCT_PRICE = 20

@app.route("/wallet", methods=["POST"])
def wallet():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid JSON"}), 400

    try:
        user = data.get("user")
    except Exception:
        return jsonify({"error": "No user received"}), 400

    return jsonify({"balance": wallets[user]}), 200

@app.route("/buy", methods=["POST"])
def buy():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid JSON"}), 400

    try:
        total = PRODUCT_PRICE * data.get("quantity")
        user = data.get("user")
    except Exception:
        return jsonify({"error": "Error con los valores recibidos"}), 400

    if total > wallets[user]:
        return jsonify({"error":"El saldo es insuficiente"}), 200
    else:
        wallets[user] = wallets[user]-total
        return jsonify({"msg":"Compra realizada correctamente"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
