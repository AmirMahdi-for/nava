from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base  
import uuid

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String(20), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")
