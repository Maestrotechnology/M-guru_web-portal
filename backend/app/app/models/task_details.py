from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey,Text,DECIMAL
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT


class TaskDetail(Base):
    __tablename__ = "task_detail"
    id = Column(Integer,primary_key=True,index=True)
    work_report_id =Column(Integer,ForeignKey("work_report.id"))
    task_id=Column(Integer,ForeignKey("task.id"))
    user_id=Column(Integer,ForeignKey("user.id"))
    
    description = Column(Text)
    status = Column(TINYINT, comment="1-> active 2 -> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    work_report = relationship("WorkReport",back_populates="task_detail")
    user = relationship("User",back_populates="task_detail")
    task = relationship("Task",back_populates="task_detail")