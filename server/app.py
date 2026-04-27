from flask import Flask, request, jsonify, render_template_string
from config.crypto_utils import decrypt_data
from datetime import datetime
import os

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
                margin: 0;
                font-family: 'Segoe UI', sans-serif;
                background: radial-gradient(circle at top, #1e293b, #020617);
                color: #e2e8f0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
            }

            h1 {
                margin-bottom: 20px;
                font-weight: 600;
            }

            .pulse {
                width: 12px;
                height: 12px;
                border-radius: 50%;
                background: #22c55e;
                box-shadow: 0 0 10px #22c55e;
                animation: pulse 1.5s infinite;
                margin-bottom: 10px;
            }

            @keyframes pulse {
                0% { transform: scale(1); opacity: 1; }
                50% { transform: scale(1.5); opacity: 0.5; }
                100% { transform: scale(1); opacity: 1; }
            }

            .card {
                background: rgba(15, 23, 42, 0.85);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(148, 163, 184, 0.2);
                padding: 30px;
                width: 450px;
                border-radius: 16px;
                box-shadow: 0 0 40px rgba(0,0,0,0.7);
            }

            .status {
                font-size: 32px;
                font-weight: bold;
                margin: 10px 0;
            }

            .yes {
                color: #22c55e;
                text-shadow: 0 0 20px #22c55e;
            }

            .no {
                color: #ef4444;
                text-shadow: 0 0 20px #ef4444;
            }

            .grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 15px;
                margin-top: 20px;
            }

            .box {
                background: #020617;
                border: 1px solid #334155;
                padding: 12px;
                border-radius: 10px;
                font-size: 13px;
            }

            .label {
                color: #94a3b8;
                font-size: 12px;
            }

            .value {
                font-size: 16px;
                margin-top: 5px;
            }
        </style>
    </head>

    <body>

        <h1>Edge AI Semantic Monitoring</h1>
        <div class="pulse"></div>

        <div class="card">

            <div>Status</div>
            <div id="status" class="status">Loading...</div>

            <div class="grid">
                <div class="box">
                    <div class="label">Confidence</div>
                    <div id="confidence" class="value"></div>
                </div>

                <div class="box">
                    <div class="label">Last Update</div>
                    <div id="timestamp" class="value"></div>
                </div>

                <div class="box">
                    <div class="label">System Mode</div>
                    <div id="mode" class="value"></div>
                </div>

                <div class="box">
                    <div class="label">Latency</div>
                    <div id="latency" class="value"></div>
                </div>

                <div class="box">
                    <div class="label">Raw Size</div>
                    <div id="raw_size" class="value"></div>
                </div>

                <div class="box">
                    <div class="label">Semantic Size</div>
                    <div id="semantic_size" class="value"></div>
                </div>
            </div>

        </div>

    <script>
        async function fetchData() {
            const response = await fetch('/latest');
            const data = await response.json();

            const statusEl = document.getElementById('status');
            statusEl.innerText = data.human_detected ? "HUMAN DETECTED" : "NO HUMAN";
            statusEl.className = "status " + (data.human_detected ? "yes" : "no");

            document.getElementById('confidence').innerText = data.confidence.toFixed(2);
            document.getElementById('timestamp').innerText = data.timestamp;
            document.getElementById('raw_size').innerText = data.raw_size + " bytes";
            document.getElementById('semantic_size').innerText = data.semantic_size + " bytes";
            document.getElementById('latency').innerText = data.latency + " sec";
            document.getElementById('mode').innerText = data.mode;
        }

        setInterval(fetchData, 1000);
        fetchData();
    </script>

    </body>
    </html>
    """)

# 🔥 THIS IS THE ONLY PART YOU WERE ASKING ABOUT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)