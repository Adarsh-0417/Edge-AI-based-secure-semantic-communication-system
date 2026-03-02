import cv2
import requests
import time
from detection import detect
from semantic_encoder import create_semantic_packet
from config.crypto_utils import encrypt_data

SERVER_URL = "http://127.0.0.1:5000/data"

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    human_detected, confidence, results = detect(frame)

    packet = create_semantic_packet("Edge-Sim-01", human_detected, confidence)

    print("Sending:", packet)

    try:
        encrypted_packet = encrypt_data(packet)
        requests.post(SERVER_URL, data=encrypted_packet)
    except:
        print("Server not running")

    annotated_frame = results[0].plot()
    cv2.imshow("Edge AI Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(1)

cap.release()
cv2.destroyAllWindows()