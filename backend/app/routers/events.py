from datetime import datetime, timezone
from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import AudioEvent
from ..schemas import AudioEventCreate, AudioEventOut
from ..services.ml_simulator import classify
from ..seed import refresh_incident
from ..services.bus import publish
router=APIRouter(prefix="/api/events", tags=["events"])
@router.get("", response_model=list[AudioEventOut])
def events(db: Session=Depends(get_db)):
    return db.query(AudioEvent).order_by(AudioEvent.timestamp.desc()).limit(100).all()
@router.post("", response_model=AudioEventOut)
async def create(payload: AudioEventCreate, db: Session=Depends(get_db)):
    ml=classify(payload.noise_type,payload.signal_level,payload.noise_quality)
    event=AudioEvent(sensor_id=payload.sensor_id,lat=payload.lat,lon=payload.lon,timestamp=payload.timestamp or datetime.now(timezone.utc),audio_filename=payload.audio_filename,signal_level=payload.signal_level,noise_quality=payload.noise_quality,source_noise_type=payload.noise_type,**ml)
    db.add(event); db.commit(); db.refresh(event); inc=refresh_incident(db)
    await publish({"type":"update","event_id":event.id,"incident_id":inc.id})
    return event
@router.post("/upload", response_model=AudioEventOut)
async def upload(sensor_id:int=Form(...), lat:float=Form(...), lon:float=Form(...), signal_level:float=Form(...), noise_quality:str=Form(...), noise_type:str=Form("unknown"), file:UploadFile|None=File(None), db:Session=Depends(get_db)):
    return await create(AudioEventCreate(sensor_id=sensor_id,lat=lat,lon=lon,signal_level=signal_level,noise_quality=noise_quality,noise_type=noise_type,audio_filename=file.filename if file else None), db)
