from sqlalchemy import  Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey,Text


class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(50))
    status = Column(TINYINT, comment="1-> active , 2-> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    created_by = Column(Integer,ForeignKey("user.id"))
    # relationship
    applications = relationship("ApplicationDetails",back_populates="courses")
    user = relationship("User",back_populates="course")
    materials = relationship("CourseMaterial",back_populates="course")
    task = relationship("Task", back_populates="course")
    assigned = relationship("AssignExam", back_populates="course")
    course_assignments = relationship("CourseAssign", back_populates="course")
    # material_access= relationship("MaterialAccess", back_populates="course")
    exam = relationship("Exam",back_populates="course")