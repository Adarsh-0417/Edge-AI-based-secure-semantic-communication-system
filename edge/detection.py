from ultralytics import YOLO

model = YOLO("models/yolov8n.pt")

def detect(frame):
    results = model(frame)

    human_detected = False
    confidence = 0.0

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            if cls == 0:
                human_detected = True
                confidence = conf

    return human_detected, confidence, results