from datetime import datetime, timezone, timedelta
from .models import Sensor, AudioEvent, Incident
from .services.ml_simulator import classify
from .services.fusion import build_hypothesis, encode_points

SENSORS = [("Точка сообщения 01",56.835,60.584),("Точка сообщения 02",56.841,60.596),("Точка сообщения 03",56.846,60.607),("Точка сообщения 04",56.852,60.619),("Точка сообщения 05",56.858,60.631),("Точка сообщения 06",56.864,60.642)]

def seed(db):
    if db.query(Sensor).count() == 0:
        for i,(name,lat,lon) in enumerate(SENSORS,1):
            db.add(Sensor(id=i,name=name,lat=lat,lon=lon,status="active",device_type="mobile_app" if i%3 else "fixed_demo_node",reliability_score=round(0.68+i*0.018,2)))
        db.commit()
    if db.query(Incident).count() == 0:
        db.add(Incident(status="Ожидание")); db.commit()
    if db.query(AudioEvent).count() == 0:
        samples=[(1,56.8348,60.5839,64,"medium","ветер"),(2,56.8412,60.5964,72,"good","похоже на БПЛА"),(3,56.8466,60.6072,78,"good","мотор")]
        for idx,s in enumerate(samples):
            ml=classify(s[5],s[3],s[4])
            db.add(AudioEvent(sensor_id=s[0],lat=s[1],lon=s[2],signal_level=s[3],noise_quality=s[4],source_noise_type=s[5],timestamp=datetime.now(timezone.utc)-timedelta(minutes=8-idx*2),**ml))
        db.commit(); refresh_incident(db)

def refresh_incident(db):
    incident = db.query(Incident).first() or Incident()
    events = db.query(AudioEvent).order_by(AudioEvent.timestamp).all()
    h = build_hypothesis(events)
    for k,v in h.items(): setattr(incident, k, encode_points(v) if k=="trajectory_points" else v)
    db.add(incident); db.commit(); db.refresh(incident)
    return incident
