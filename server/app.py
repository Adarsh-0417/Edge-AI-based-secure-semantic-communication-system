from flask import Flask, request, jsonify, render_template_string
from config.crypto_utils import decrypt_data
from datetime import datetime

app = Flask(__name__)

latest_data = {
    "human_detected": False,
    "confidence": 0.0,
    "timestamp": "N/A",
    "raw_size": 0,
    "semantic_size": 0,
    "latency": 0,
    "mode": "N/A"
}

@app.route("/data", methods=["POST"])
def receive():
    global latest_data
    try:
        encrypted_data = request.data
        packet_size = len(encrypted_data)

        data = decrypt_data(encrypted_data)

        latest_data = {
            "human_detected": data.get("human_detected"),
            "confidence": data.get("confidence"),
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "raw_size": data.get("raw_size"),
            "semantic_size": data.get("semantic_size"),
            "latency": data.get("latency"),
            "mode": data.get("mode")
        }

        return jsonify({"status": "ok"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/latest", methods=["GET"])
def latest():
    return jsonify(latest_data)


@app.route("/")
def dashboard():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Semantic Disaster Dashboard</title>
        <style>
            body {
                font-family: Arial;
                background: #0f172a;
                color: white;
                text-align: center;
                padding-top: 50px;
            }
            .card {
                background: #111827;
                border: 1px solid #334155;
                padding: 30px;
                margin: 20px auto;
                width: 400px;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0,0,0,0.5);
            }
            .status {
                font-size: 28px;
                font-weight: bold;
            }
            .yes { 
            color: #22c55e;
            text-shadow: 0 0 10px #22c55e;
            }
            .no { 
            color: #ef4444;
            text-shadow: 0 0 10px #ef4444;
            }
        </style>
    </head>
    <body>

        <h1>Edge AI Semantic Monitoring</h1>

        <div class="card">
            <div>Status:</div>
            <div id="status" class="status">Loading...</div>

            <p>Confidence: <span id="confidence"></span></p>
            <p>Last Update: <span id="timestamp"></span></p>

            <hr>

            <p><strong>System Mode:</strong> <span id="mode"></span></p>
            <p>Raw Frame Size: <span id="raw_size"></span> bytes</p>
            <p>Semantic Packet Size: <span id="semantic_size"></span> bytes</p>
            <p>Processing Latency: <span id="latency"></span> sec</p>
        </div>

        <script>
            async function fetchData() {
                const response = await fetch('/latest');
                const data = await response.json();

                const statusEl = document.getElementById('status');
                statusEl.innerText = data.human_detected ? "HUMAN DETECTED" : "NO HUMAN";

                statusEl.className = "status " + (data.human_detected ? "yes" : "no");
                                  
                document.getElementById('confidence').innerText = data.confidence;
                document.getElementById('timestamp').innerText = data.timestamp;
                document.getElementById('raw_size').innerText = data.raw_size;
                document.getElementById('semantic_size').innerText = data.semantic_size;
                document.getElementById('latency').innerText = data.latency;
                document.getElementById('mode').innerText = data.mode;
            }

            setInterval(fetchData, 1000);
            fetchData();
        </script>

    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(port=5000, debug=True)