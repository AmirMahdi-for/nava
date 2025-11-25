from sqlalchemy import (
    Column, Integer, String, ForeignKey, Enum, Text, Float, DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base  
import enum

class ModelRequestTypeEnum(str, enum.Enum):
    tts = "tts"
    stt = "stt"
    llm = "llm"

class ModelRequest(Base):
    __tablename__ = "model_requests"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"))
    type = Column(Enum(ModelRequestTypeEnum))
    request_payload = Column(Text)
    response_payload = Column(Text)
    per_token = Column(Float, default=0.0)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    message = relationship("Message", back_populates="model_requests")
