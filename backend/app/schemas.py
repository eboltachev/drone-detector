from datetime import datetime, timezone
from pydantic import BaseModel, Field

class SensorOut(BaseModel):
    id: int; name: str; lat: float; lon: float; status: str; device_type: str; reliability_score: float
    model_config = {"from_attributes": True}

class AudioEventCreate(BaseModel):
    sensor_id: int
    lat: float
    lon: float
    timestamp: datetime | None = None
    audio_filename: str | None = None
    signal_level: float = Field(ge=0, le=100)
    noise_quality: str
    noise_type: str = "unknown"

class AudioEventOut(BaseModel):
    id: int; sensor_id: int; timestamp: datetime; lat: float; lon: float; audio_filename: str | None
    signal_level: float; noise_quality: str; source_noise_type: str; predicted_class: str; confidence: float; processing_status: str
    model_config = {"from_attributes": True}

class IncidentOut(BaseModel):
    id: int; started_at: datetime; status: str; predicted_type: str; confidence: float
    trajectory_points: list[dict[str, float]]; direction_bearing: float; last_update_at: datetime; hypothesis_message_count: int

class ManualEventForm(BaseModel):
    sensor_id: int
    lat: float
    lon: float
    timestamp: datetime | None = None
    signal_level: float
    noise_quality: str
    noise_type: str = "unknown"
