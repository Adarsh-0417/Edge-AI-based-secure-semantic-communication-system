# Edge AI Secure Semantic Communication System

This project demonstrates a simple **Edge AI + Semantic Communication pipeline** for low-bandwidth environments.

Instead of sending raw images, the system:

* detects humans using YOLO (edge side)
* converts output into a small semantic packet
* encrypts it using AES
* sends it to a server
* displays it on a live dashboard

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
