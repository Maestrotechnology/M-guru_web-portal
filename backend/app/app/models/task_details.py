from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey,Text,DECIMAL
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT


class TaskDetail(Base):
    __tablename__ = "task_detail"
    id = Column(Integer,primary_key=True,index=True)
    attendance_id =Column(Integer,ForeignKey("attendance.id"))
    task_id=Column(Integer,ForeignKey("task.id"))
    user_id=Column(Integer,ForeignKey("user.id"))
    expected_time=Column(String(50))
    priority=Column(TINYINT,comment="1-> High 2 -> medium 3 -> low" )
    complete_status = Column(TINYINT, comment="1-> complete 2 -> not complete")
    description = Column(Text)
    status = Column(TINYINT, comment="1-> active 2 -> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    attendance = relationship("Attendance",back_populates="task_detail")
    user = relationship("User",back_populates="task_detail")
    task = relationship("Task",back_populates="task_detail")
    work_history = relationship("WorkHistory",back_populates="task_detail")


