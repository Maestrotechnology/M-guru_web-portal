from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey,Text,DECIMAL
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT


class TaskDetail(Base):
    __tablename__ = "task_detail"
    id = Column(Integer,primary_key=True,index=True)
    attendance_id =Column(Integer,ForeignKey("attendance.id"))
   
    user_id=Column(Integer,ForeignKey("user.id"))
    expected_time=Column(String(50))
    trainer_id=Column(Integer,ForeignKey("user.id"))
    rating=Column(Integer)
    close_status=Column(TINYINT, comment="1-> close ")
    complete_status = Column(TINYINT, comment="1-> complete  ")
    description = Column(Text)
    status = Column(TINYINT, comment="1-> active 2 -> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    attendance = relationship("Attendance",back_populates="task_detail")
    user = relationship("User",foreign_keys=[user_id],back_populates="task_detail")
    users = relationship("User",foreign_keys=[trainer_id],back_populates="task_details")
    work_history = relationship("WorkHistory",back_populates="task_detail")



