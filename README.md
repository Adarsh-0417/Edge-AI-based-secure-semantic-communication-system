# 🚀 Edge AI-Based Secure Semantic Communication System

A real-time **Edge AI + Semantic Communication framework** designed for **low-bandwidth disaster response environments**.

Instead of transmitting raw images or video streams, this system performs **on-device inference** and sends only **compact, encrypted semantic data**, enabling faster and more reliable communication under constrained network conditions.

---

## 🧠 Key Idea

> *Transmit meaning, not data.*

Traditional systems send raw multimedia → high bandwidth → high latency
This system sends **semantic insights** → low bandwidth → fast response

---

## ⚙️ System Architecture

```
Camera (Edge Device)
        ↓
YOLOv8 Detection (Edge AI)
        ↓
Semantic Encoding (JSON)
        ↓
AES Encryption
        ↓
HTTP Transmission
        ↓
Cloud Server (Flask)
        ↓
Real-Time Dashboard
```

---

## ✨ Features

* 🔍 Real-time **human detection** using YOLOv8
* 🧠 **Semantic encoding** (transmit only meaningful data)
* 🔐 **AES encryption** for secure communication
* 🌐 **Cloud-based monitoring dashboard**
* ⚡ **Low latency & bandwidth-efficient communication**
* 📊 Real-time metrics:

  * Detection status
  * Confidence score
  * Latency
  * Packet size comparison

---

## 📁 Project Structure

```
├── config/
│   ├── crypto_utils.py
│   └── settings.py
│
├── edge/
│   ├── detection.py
│   ├── semantic_encoder.py
│   └── edge_main.py
│
├── server/
│   └── app.py
│
├── models/
│   └── yolov8n.pt
│
├── requirements.txt
├── Procfile
└── README.md
```

---

## 🛠️ Tech Stack

* Python
* Flask (Backend API)
* OpenCV (Video Processing)
* Ultralytics YOLOv8 (Edge AI)
* AES Encryption (Security)
* HTML + JS (Dashboard)

---

## 🚀 Getting Started (Local Setup)

### 1️⃣ Clone the repository

```
git clone <your-repo-link>
cd Edge-AI-based-secure-semantic-communication-system
```

### 2️⃣ Create virtual environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

## ▶️ Run the System

### Start Server

```
python -m server.app
```

### Start Edge Device

```
python -m edge.edge_main
```

Open dashboard:

```
http://127.0.0.1:5000
```

---

## 🌐 Deployment (Railway)

1. Push code to GitHub
2. Connect repo to Railway
3. Ensure files:

   * `requirements.txt`
   * `Procfile`

### Procfile

```
web: python -m server.app
```

### After deployment:

* Update edge URL:

```
https://your-app.up.railway.app/data
```

---

## 📊 Performance Highlights

| Metric          | Value          |
| --------------- | -------------- |
| Raw Frame Size  | ~80–200 KB     |
| Semantic Packet | ~150–300 bytes |
| Data Reduction  | ~500x – 1000x  |
| Latency         | ~0.1 sec       |

---

## ⚠️ Limitations

* Single-class detection (human only)
* Simulated environment (not full disaster network)
* Requires active internet connection

---

## 🔮 Future Scope

* Multi-object detection (fire, vehicles, hazards)
* Raspberry Pi deployment (true edge hardware)
* MQTT / LoRa integration
* Real disaster network simulation
* AI-based semantic compression

---

## 🎯 Applications

* Disaster response systems
* Smart city surveillance
* Defense & security monitoring
* IoT-based emergency communication

---

## 👨‍💻 Authors

* Adarsh Sharma
* Taarini Mishra
* Vaibhav Katariya

---

## 📜 License

This project is for academic and research purposes.
