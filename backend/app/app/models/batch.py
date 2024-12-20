from sqlalchemy import  Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT


class Batch(Base):
    __tablename__ = "batch"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(50))
    description = Column(String(350))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    fee = Column(Integer)

    status = Column(TINYINT, comment="1-> active , 2-> delete")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # relationship
    users = relationship("User",back_populates="batch")
    applications = relationship("ApplicationDetails",back_populates="batch")
    task = relationship("Task",back_populates="batch")
    course_material = relationship("CourseMaterial",back_populates="batch")
    work_report = relationship("WorkReport",back_populates="batch")
    assigned_exams = relationship("AssignExam",back_populates="batch")
    
