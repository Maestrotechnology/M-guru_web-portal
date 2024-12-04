from sqlalchemy.orm import relationship
from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class StudentProjectDetail(Base):
    __tablename__ = "student_project_detail"

    id = Column(Integer,primary_key=True,index=True)
    mark = Column(Integer)
    project_url = Column(String(255))
    project_start_date = Column(DateTime)
    project_end_date = Column(DateTime)
    description = Column(String(255))

    status = Column(TINYINT, comment="1-> active 2 -> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # ForeignKey
    task_id = Column(Integer,ForeignKey("task.id"))
    user_id = Column(Integer,ForeignKey("user.id"))

    # relationship
    task = relationship("Task", back_populates="project_details")
    student = relationship("User",back_populates="project_details")
    
