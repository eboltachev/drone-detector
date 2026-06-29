import json, math
from collections import Counter

def _bearing(a, b):
    lat1, lat2 = math.radians(a.lat), math.radians(b.lat)
    dlon = math.radians(b.lon - a.lon)
    y = math.sin(dlon) * math.cos(lat2)
    x = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dlon)
    return (math.degrees(math.atan2(y, x)) + 360) % 360

def direction_name(bearing: float) -> str:
    names = ["север", "северо-восток", "восток", "юго-восток", "юг", "юго-запад", "запад", "северо-запад"]
    return names[round(bearing / 45) % 8]

def build_hypothesis(events):
    relevant = [e for e in events if e.predicted_class == "drone_like"][-8:]
    if len(relevant) < 2:
        return {"status": "Недостаточно данных", "predicted_type": "unknown", "confidence": 0.0, "trajectory_points": [], "direction_bearing": 0.0, "hypothesis_message_count": len(relevant)}
    ordered = sorted(relevant, key=lambda e: e.timestamp)
    points = [{"lat": e.lat, "lon": e.lon} for e in ordered]
    avg = sum(e.confidence for e in ordered) / len(ordered)
    confidence = min(0.92, avg + min(len(ordered), 6) * 0.035)
    bearing = _bearing(ordered[0], ordered[-1]) if len(ordered) > 1 else 0.0
    return {"status": "Гипотеза построена" if len(ordered) >= 3 else "Сбор данных", "predicted_type": Counter(e.predicted_class for e in ordered).most_common(1)[0][0], "confidence": round(confidence, 2), "trajectory_points": points, "direction_bearing": round(bearing, 1), "hypothesis_message_count": len(ordered)}

def encode_points(points):
    return json.dumps(points, ensure_ascii=False)

def decode_points(raw):
    try: return json.loads(raw or "[]")
    except json.JSONDecodeError: return []
