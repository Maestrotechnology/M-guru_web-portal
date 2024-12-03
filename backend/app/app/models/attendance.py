from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey,Text,DECIMAL
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer,primary_key=True,index=True)
    check_in=Column(DateTime)
    check_out=Column(DateTime)
    task_id=Column(Integer,ForeignKey("task.id"))
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
    work_status= Column(TINYINT, comment="1-> chek_in 2 -> check_out")
    users = relationship("User",back_populates="attendance")
    work_history = relationship("WorkHistory",back_populates="attendance")

    task = relationship("Task",back_populates="attendance")
    task_detail = relationship("TaskDetail",back_populates="attendance")
    