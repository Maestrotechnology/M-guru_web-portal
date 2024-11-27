from sqlalchemy import  Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT

from app.db.base_class import Base

class ApiTokens(Base):
    __tablename__ = "api_tokens"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("user.id"))
    
    token=Column(String(100))
    created_at=Column(DateTime)
    renewed_at=Column(DateTime)
    device_type=Column(TINYINT(1), comment="1-Android, 2-iOS", nullable=False)
    validity=Column(TINYINT(1),comment="0-Expired, 1- Lifetime", nullable=False)
    device_id=Column(String(255))
    push_device_id=Column(String(255))
    device_ip=Column(String(255))
    status=Column(TINYINT(1),comment="1-active, -1 inactive, 0- deleted", nullable=False)

    user=relationship("User",back_populates="api_tokens")
    