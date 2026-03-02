def create_semantic_packet(device_id, human_detected, confidence):
    return {
        "device_id": device_id,
        "human_detected": human_detected,
        "confidence": round(confidence, 3)
    }