QUALITY_FACTOR = {"good": 1.0, "medium": 0.74, "low": 0.45, "хорошая": 1.0, "средняя": 0.74, "низкая": 0.45}
CLASS_MAP = {"мотор": "drone_like", "похоже на БПЛА": "drone_like", "drone_like": "drone_like", "транспорт": "vehicle_noise", "vehicle": "vehicle_noise", "ветер": "wind_noise", "wind": "wind_noise"}

def classify(noise_type: str, signal_level: float, noise_quality: str) -> dict:
    predicted = CLASS_MAP.get(noise_type, "unknown")
    base = {"drone_like": 0.62, "vehicle_noise": 0.55, "wind_noise": 0.5, "unknown": 0.28}[predicted]
    signal_boost = min(max(signal_level, 0), 100) / 100 * 0.25
    confidence = min(0.95, (base + signal_boost) * QUALITY_FACTOR.get(noise_quality, 0.65))
    return {"predicted_class": predicted, "confidence": round(confidence, 2), "processing_status": "processed_by_synthetic_ml"}
