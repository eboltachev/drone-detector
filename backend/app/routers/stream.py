from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from ..services.bus import event_generator
router=APIRouter(tags=["stream"])
@router.get("/api/stream")
async def stream():
    return StreamingResponse(event_generator(), media_type="text/event-stream")
