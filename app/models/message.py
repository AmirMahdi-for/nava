from sqlalchemy import (
    Column, Integer, String, ForeignKey, Enum, Text, DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base
import enum

class MessageFromEnum(str, enum.Enum):
    server = "server"
    client = "client"

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    audio_url = Column(String(255))
    text = Column(Text, nullable=True)
    from_user = Column(Enum(MessageFromEnum))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    conversation = relationship("Conversation", back_populates="messages")
    model_requests = relationship("ModelRequest", back_populates="message")
    audio_file = relationship("AudioFile", back_populates="message", uselist=False)
