🚀 Edge AI-Based Secure Semantic Communication System

A real-time Edge AI + Semantic Communication framework designed for low-bandwidth disaster response environments.

Instead of transmitting raw images or video streams, this system performs on-device inference and sends only compact, encrypted semantic data, enabling faster and more reliable communication under constrained network conditions.

🧠 Key Idea

Transmit meaning, not data.

Traditional systems send raw multimedia → high bandwidth → high latency
This system sends semantic insights → low bandwidth → fast response

---

## 🔧 Project Structure

```
config/        → encryption + settings
edge/          → detection + semantic encoding + sender
server/        → Flask backend + dashboard
models/        → YOLO model
```

---

## ⚙️ Requirements

Install dependencies:

```
pip install -r requirements.txt
```

---

## ▶️ How to Run (IMPORTANT)

You must run **both server and edge separately**.

### 1. Start Server (Terminal 1)

```
python -m server.app
```

---

### 2. Start Edge Device (Terminal 2)

```
python -m edge.edge_main
```

---

### 3. Open Dashboard

```
http://127.0.0.1:5000
```

---

## 🌐 Deployment

Backend is deployed using Railway.

After deployment, update URL inside edge code:

```
url = "https://your-railway-url.up.railway.app/data"
```

Then run only:

```
python -m edge.edge_main
```

Dashboard will be available online.

---

## 📊 Output

Dashboard shows:

* Human detected / not detected
* Confidence score
* Latency
* Raw vs semantic data size

---

## ⚠️ Notes

* YOLO runs only on edge device (not on server)
* Server only receives and displays data
* Requires internet when using deployed backend

---

## 👨‍💻 Authors

* Adarsh Sharma
* Team Members
