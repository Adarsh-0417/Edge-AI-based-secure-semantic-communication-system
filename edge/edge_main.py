import cv2
import requests
import time

from edge.detection import detect
from edge.semantic_encoder import create_semantic_packet
from config.crypto_utils import encrypt_data

SERVER_URL = "http://127.0.0.1:5000/data"

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not detected")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Step 1: Detect
    human_detected, confidence, results = detect(frame)

    # Step 2: Create semantic packet
    packet = create_semantic_packet(
        "Edge-Sim-01",
        human_detected,
        confidence
    )

    # Step 3: Encrypt packet
    encrypted_packet = encrypt_data(packet)

    # 🔐 This is what encrypted data looks like
    print("Encrypted Packet:", encrypted_packet)
    print("Encrypted Length:", len(encrypted_packet))

    # Step 4: Send encrypted bytes
    try:
        requests.post(SERVER_URL, data=encrypted_packet)
    except:
        print("Server not running")

    # Show detection window
    annotated_frame = results[0].plot()
    cv2.imshow("Edge AI Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(1)

cap.release()
cv2.destroyAllWindows()