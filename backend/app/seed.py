from datetime import datetime, timezone, timedelta
from .models import Sensor, AudioEvent, Incident
from .services.ml_simulator import classify
from .services.fusion import build_hypothesis, encode_points

SENSORS = [("Сенсор А-01",55.751,37.602),("Сенсор А-02",55.759,37.617),("Сенсор А-03",55.744,37.629),("Сенсор А-04",55.735,37.606),("Сенсор А-05",55.766,37.591),("Сенсор А-06",55.728,37.642),("Сенсор А-07",55.773,37.636),("Сенсор А-08",55.748,37.573),("Сенсор А-09",55.731,37.581),("Сенсор А-10",55.762,37.659),("Сенсор А-11",55.719,37.619),("Сенсор А-12",55.781,37.608)]

def seed(db):
    if db.query(Sensor).count() == 0:
        for i,(name,lat,lon) in enumerate(SENSORS,1):
            db.add(Sensor(id=i,name=name,lat=lat,lon=lon,status="active",device_type="mobile_app" if i%3 else "fixed_demo_node",reliability_score=round(0.68+i*0.018,2)))
        db.commit()
    if db.query(Incident).count() == 0:
        db.add(Incident(status="Ожидание")); db.commit()
    if db.query(AudioEvent).count() == 0:
        samples=[(1,55.742,37.585,64,"medium","ветер"),(3,55.748,37.598,72,"good","похоже на БПЛА"),(5,55.755,37.613,78,"good","мотор")]
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
