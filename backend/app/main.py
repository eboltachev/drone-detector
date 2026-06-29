from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import Base, engine, SessionLocal
from .seed import seed
from .routers import sensors, events, incidents, scenario, stream

app=FastAPI(title="Crowdsourced Acoustic UAV Detection Demo", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=settings.origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db=SessionLocal()
    try: seed(db)
    finally: db.close()

@app.get("/api/health")
def health():
    return {"status":"ok", "mode":"DEMO synthetic data only"}

app.include_router(sensors.router); app.include_router(events.router); app.include_router(incidents.router); app.include_router(scenario.router); app.include_router(stream.router)
