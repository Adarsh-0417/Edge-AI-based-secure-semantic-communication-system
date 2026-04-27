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
    background: #020617;
    color: white;
    display: flex;
}

/* SIDEBAR */
.sidebar {
    width: 220px;
    height: 100vh;
    background: #020617;
    border-right: 1px solid #1e293b;
    padding: 20px;
}

.sidebar h2 {
    font-size: 16px;
    margin-bottom: 20px;
    color: #94a3b8;
}

.menu-item {
    padding: 10px;
    border-radius: 8px;
    margin-bottom: 10px;
    cursor: pointer;
}

.menu-item:hover {
    background: #0f172a;
}

/* MAIN */
.main {
    flex: 1;
    padding: 30px;
}

/* TOP BAR */
.top {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
}

.search {
    background: #0f172a;
    border: none;
    padding: 10px;
    border-radius: 8px;
    color: white;
}

/* GRID */
.grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 20px;
}

/* CAMERA */
.camera {
    background: #0f172a;
    padding: 20px;
    border-radius: 16px;
}

.status {
    margin-top: 10px;
    font-size: 20px;
    font-weight: bold;
}

.yes {
    color: #22c55e;
}

.no {
    color: #ef4444;
}

/* RIGHT PANEL */
.panel {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.card {
    background: #0f172a;
    padding: 15px;
    border-radius: 12px;
}

.label {
    color: #94a3b8;
    font-size: 12px;
}

.value {
    font-size: 16px;
    margin-top: 5px;
}

/* GRAPH FAKE */
.graph {
    height: 120px;
    background: linear-gradient(to right, #0ea5e9, transparent);
    border-radius: 10px;
    margin-top: 10px;
}
</style>
</head>

<body>

<!-- SIDEBAR -->
<div class="sidebar">
    <h2>Disaster Watch</h2>
    <div class="menu-item">Dashboard</div>
    <div class="menu-item">Statistics</div>
    <div class="menu-item">Alerts</div>
    <div class="menu-item">History</div>
</div>

<!-- MAIN -->
<div class="main">

    <div class="top">
        <h2>Edge AI Monitoring</h2>
        <input class="search" placeholder="Search...">
    </div>

    <div class="grid">

        <!-- LEFT CAMERA + STATUS -->
        <div class="camera">
            <h3>Camera Feed</h3>
            <p class="status" id="status">Loading...</p>
        </div>

        <!-- RIGHT PANEL -->
        <div class="panel">

            <div class="card">
                <div class="label">Confidence</div>
                <div id="confidence" class="value"></div>
            </div>

            <div class="card">
                <div class="label">Last Update</div>
                <div id="timestamp" class="value"></div>
            </div>

            <div class="card">
                <div class="label">Latency</div>
                <div id="latency" class="value"></div>
            </div>

            <div class="card">
                <div class="label">Raw Size</div>
                <div id="raw_size" class="value"></div>
            </div>

            <div class="card">
                <div class="label">Semantic Size</div>
                <div id="semantic_size" class="value"></div>
            </div>

            <div class="card">
                <div class="label">System Mode</div>
                <div id="mode" class="value"></div>
            </div>

        </div>

    </div>

</div>

<script>
async function fetchData() {
    const res = await fetch('/latest');
    const data = await res.json();

    const statusEl = document.getElementById('status');

    statusEl.innerText = data.human_detected ? "HUMAN DETECTED" : "NO HUMAN";
    statusEl.className = "status " + (data.human_detected ? "yes" : "no");

    document.getElementById('confidence').innerText = data.confidence.toFixed(2);
    document.getElementById('timestamp').innerText = data.timestamp;
    document.getElementById('latency').innerText = data.latency + " sec";
    document.getElementById('raw_size').innerText = data.raw_size + " bytes";
    document.getElementById('semantic_size').innerText = data.semantic_size + " bytes";
    document.getElementById('mode').innerText = data.mode;
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