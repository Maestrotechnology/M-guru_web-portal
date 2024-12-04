from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey,Text,DECIMAL
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT


class WorkHistory(Base):
    __tablename__ = "work_history"

    id = Column(Integer,primary_key=True,index=True)
    attendance_id = Column(Integer,ForeignKey("attendance.id"))
    break_time=Column(DateTime)
    breakEnd_time=Column(DateTime)
    work_time=Column(DateTime)
    workEnd_time=Column(DateTime)
    Ispaused = Column(TINYINT, comment="1-> yes 2 -> no")
    status = Column(TINYINT, comment="1-> active 2 -> inactive")
    taskDetail_id=Column(Integer,ForeignKey("task_detail.id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    attendance = relationship("Attendance",back_populates="work_history")
    task_detail = relationship("TaskDetail",back_populates="work_history")

    
    