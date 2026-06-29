from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Sensor(Base):
    __tablename__ = "sensors"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(40), default="active")
    device_type: Mapped[str] = mapped_column(String(80), default="mobile_app")
    reliability_score: Mapped[float] = mapped_column(Float, default=0.8)

class AudioEvent(Base):
    __tablename__ = "audio_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sensor_id: Mapped[int] = mapped_column(ForeignKey("sensors.id"))
    timestamp: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())
    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)
    audio_filename: Mapped[str | None] = mapped_column(String(255), nullable=True)
    signal_level: Mapped[float] = mapped_column(Float)
    noise_quality: Mapped[str] = mapped_column(String(40))
    source_noise_type: Mapped[str] = mapped_column(String(60), default="unknown")
    predicted_class: Mapped[str] = mapped_column(String(60))
    confidence: Mapped[float] = mapped_column(Float)
    processing_status: Mapped[str] = mapped_column(String(60), default="processed_demo")

class Incident(Base):
    __tablename__ = "incidents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    started_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())
    status: Mapped[str] = mapped_column(String(80), default="Ожидание")
    predicted_type: Mapped[str] = mapped_column(String(80), default="unknown")
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    trajectory_points: Mapped[str] = mapped_column(Text, default="[]")
    direction_bearing: Mapped[float] = mapped_column(Float, default=0.0)
    last_update_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    hypothesis_message_count: Mapped[int] = mapped_column(Integer, default=0)
