from sqlalchemy import (
    Column, Integer, String, ForeignKey, Enum, Text, Float, DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base  

class ReqLog(Base):
    __tablename__ = "req_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    endpoint = Column(String(255))
    ip = Column(String(45))
    per_token = Column(Float, default=0.0)
    status_code = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="req_logs")

