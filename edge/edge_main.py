import cv2
import requests
import time

from edge.detection import detect
from edge.semantic_encoder import create_semantic_packet
from config.crypto_utils import encrypt_data

SERVER_URL = "https://melodious-rebirth-production.up.railway.app/"

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not detected")
    exit()
cv2.namedWindow("Edge AI Detection", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Edge AI Detection", 400, 300)

while True:
    start_time = time.time()

    ret, frame = cap.read()
    if not ret:
        break

    # RAW FRAME SIZE (compressed JPEG)
    _, img_encoded = cv2.imencode('.jpg', frame)
    raw_size = len(img_encoded.tobytes())

    # Detection
    human_detected, confidence, results = detect(frame)

    # Semantic packet
    packet = create_semantic_packet(
        "Edge-Sim-01",
        human_detected,
        confidence
    )

    # Encrypt
    encrypted_packet = encrypt_data(packet)
    semantic_size = len(encrypted_packet)

    # Latency
    total_latency = round(time.time() - start_time, 4)

    # Create enhanced transmission packet
    enhanced_packet = {
        "human_detected": human_detected,
        "confidence": confidence,
        "raw_size": raw_size,
        "semantic_size": semantic_size,
        "latency": total_latency,
        "mode": "Semantic Encrypted"
    }

    encrypted_final = encrypt_data(enhanced_packet)

    try:
        requests.post(SERVER_URL, data=encrypted_final)
    except:
        print("Server not running")

    print("Raw:", raw_size,
          "| Semantic:", semantic_size,
          "| Latency:", total_latency)

    annotated_frame = results[0].plot()
    cv2.imshow("Edge AI Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(1)

cap.release()
cv2.destroyAllWindows()