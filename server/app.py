from flask import Flask, request, jsonify
from config.crypto_utils import decrypt_data

app = Flask(__name__)

@app.route("/data", methods=["POST"])
def receive():
    encrypted_data = request.data
    data = decrypt_data(encrypted_data)

    print("Received:", data)

    if data.get("human_detected"):
        print("ALERT: Human detected!")
    else:
        print("No human detected.")

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)