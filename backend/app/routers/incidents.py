from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Incident
from ..schemas import IncidentOut
from ..services.fusion import decode_points
router=APIRouter(prefix="/api/incidents", tags=["incidents"])
@router.get("/current", response_model=IncidentOut)
def current(db: Session=Depends(get_db)):
    i=db.query(Incident).first()
    return IncidentOut(id=i.id,started_at=i.started_at,status=i.status,predicted_type=i.predicted_type,confidence=i.confidence,trajectory_points=decode_points(i.trajectory_points),direction_bearing=i.direction_bearing,last_update_at=i.last_update_at,hypothesis_message_count=i.hypothesis_message_count)
