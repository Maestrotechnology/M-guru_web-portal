from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey,Text,DECIMAL
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT


class WorkReport(Base):
    __tablename__ = "work_report"

    id = Column(Integer,primary_key=True,index=True)
    check_in=Column(DateTime)
    check_out=Column(DateTime)
    task=Column(String(255))
    description = Column(Text)
    work_time=Column(Integer)
    break_time=Column(Integer)
    in_ip = Column(String(255))
    out_ip = Column(String(255))
    in_latitude = Column(DECIMAL(15, 7))
    in_longitude = Column(DECIMAL(15, 7))
    out_latitude = Column(DECIMAL(15, 7))
    out_longitude = Column(DECIMAL(15, 7))
    status = Column(TINYINT, comment="1-> active 2 -> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    user_id = Column(Integer,ForeignKey("user.id"))

    users = relationship("User",back_populates="work_report")
    work_history = relationship("WorkHistory",back_populates="work_report")
    