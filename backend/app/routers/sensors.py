from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Sensor
from ..schemas import SensorOut
router=APIRouter(prefix="/api/sensors", tags=["sensors"])
@router.get("", response_model=list[SensorOut])
def sensors(db: Session=Depends(get_db)):
    return db.query(Sensor).order_by(Sensor.id).all()
