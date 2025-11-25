from sqlalchemy import (
    Column, Integer, String, ForeignKey, Float, DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base  

class AudioFile(Base):
    __tablename__ = "audio_files"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"))
    size = Column(Integer)
    format = Column(String(20))
    path = Column(String(255))
    duration = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    message = relationship("Message", back_populates="audio_file")
