from flask import Flask, request, jsonify, render_template_string
from config.crypto_utils import decrypt_data
from datetime import datetime
import pytz
import os

app = Flask(__name__)

IST = pytz.timezone("Asia/Kolkata")

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

        current_time = datetime.now(IST).strftime("%I:%M:%S %p")

        latest_data = {
            "human_detected": data.get("human_detected"),
            "confidence": data.get("confidence"),
            "timestamp": current_time,
            "raw_size": data.get("raw_size"),
            "semantic_size": data.get("semantic_size"),
            "latency": data.get("latency"),
            "mode": data.get("mode")
        }

        return jsonify({"status": "ok"})

    except Exception as e:
        print("ERROR:", e)
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
<title>Edge AI Dashboard</title>

<style>
body {
    margin: 0;
    font-family: 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #020617, #0f172a);
    color: white;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 40px;
}

h1 {
    font-size: 28px;
    margin-bottom: 10px;
}

.live {
    width: 10px;
    height: 10px;
    background: #22c55e;
    border-radius: 50%;
    box-shadow: 0 0 12px #22c55e;
    margin-bottom: 20px;
}

/* MAIN CARD */
.container {
    display: flex;
    gap: 20px;
}

/* LEFT STATUS */
.status-card {
    background: rgba(15,23,42,0.9);
    padding: 30px;
    border-radius: 16px;
    border: 1px solid #334155;
    width: 250px;
    text-align: center;
    box-shadow: 0 0 25px rgba(0,0,0,0.7);
}

.status-text {
    font-size: 26px;
    font-weight: bold;
    margin-top: 10px;
}

.yes {
    color: #22c55e;
    text-shadow: 0 0 15px #22c55e;
}

.no {
    color: #ef4444;
    text-shadow: 0 0 15px #ef4444;
}

/* RIGHT GRID */
.grid {
    display: grid;
    grid-template-columns: repeat(2, 180px);
    gap: 15px;
}

.box {
    background: rgba(2,6,23,0.9);
    border: 1px solid #334155;
    padding: 15px;
    border-radius: 12px;
    box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
}

.label {
    font-size: 12px;
    color: #94a3b8;
}

.value {
    font-size: 16px;
    margin-top: 5px;
}

/* Hover effect */
.box:hover {
    transform: scale(1.05);
    transition: 0.2s;
}
</style>
</head>

<body>

<h1>Edge AI Semantic Monitoring</h1>
<div class="live"></div>

<div class="container">

    <!-- STATUS -->
    <div class="status-card">
        <div>Status</div>
        <div id="status" class="status-text">Loading...</div>
    </div>

    <!-- DATA -->
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
    const res = await fetch('/latest');
    const data = await res.json();

    const statusEl = document.getElementById('status');

    statusEl.innerText = data.human_detected ? "HUMAN DETECTED" : "NO HUMAN";
    statusEl.className = "status-text " + (data.human_detected ? "yes" : "no");

    document.getElementById('confidence').innerText = data.confidence.toFixed(2);
    document.getElementById('timestamp').innerText = data.timestamp;
    document.getElementById('mode').innerText = data.mode;
    document.getElementById('latency').innerText = data.latency + " sec";
    document.getElementById('raw_size').innerText = data.raw_size + " bytes";
    document.getElementById('semantic_size').innerText = data.semantic_size + " bytes";
}

setInterval(fetchData, 1000);
fetchData();
</script>

</body>
</html>
""")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)