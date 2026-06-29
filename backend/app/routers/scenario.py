import asyncio
from datetime import datetime, timezone
from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal, get_db
from ..models import AudioEvent
from ..schemas import AudioEventCreate
from ..routers.events import create
from ..seed import refresh_incident
from ..services.bus import publish
router=APIRouter(prefix="/api/scenario", tags=["scenario"])
SCENARIO=[(2,55.739,37.575,58,"medium","транспорт"),(4,55.744,37.589,70,"good","похоже на БПЛА"),(6,55.750,37.604,76,"good","мотор"),(8,55.756,37.621,82,"good","похоже на БПЛА"),(10,55.762,37.637,74,"medium","мотор"),(12,55.768,37.651,67,"low","похоже на БПЛА")]
async def run_scenario():
    for item in SCENARIO:
        await asyncio.sleep(1.3)
        db=SessionLocal()
        try:
            await create(AudioEventCreate(sensor_id=item[0],lat=item[1],lon=item[2],signal_level=item[3],noise_quality=item[4],noise_type=item[5],timestamp=datetime.now(timezone.utc)), db)
        finally: db.close()
@router.post("/start")
async def start(background: BackgroundTasks):
    background.add_task(run_scenario)
    await publish({"type":"scenario_started"})
    return {"status":"started", "message":"synthetic scenario is running"}
@router.post("/reset")
async def reset(db: Session=Depends(get_db)):
    db.query(AudioEvent).delete(); db.commit(); inc=refresh_incident(db); await publish({"type":"reset","incident_id":inc.id}); return {"status":"reset"}
