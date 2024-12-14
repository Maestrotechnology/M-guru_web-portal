from sqlalchemy.orm import relationship
from sqlalchemy import  Column, Integer, String, DateTime, ForeignKey
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT


class AssignExam(Base):
    __tablename__ = "assign_exam"

    id = Column(Integer, primary_key=True, index=True)

    status = Column(TINYINT, comment="1-> active , 2-> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    batch_id = Column(Integer, ForeignKey("batch.id"),index=True)
    exam_id = Column(Integer, ForeignKey("exam.id"), index=True)
    set_id = Column(Integer, ForeignKey("set.id"),index=True)
    course_id = Column(Integer, ForeignKey("course.id"),index=True)
    student_id = Column(Integer, ForeignKey("user.id"), index=True)

    # relationship
    batch = relationship("Batch",back_populates="assigned_exams")
    exam = relationship("Exam", back_populates="assigned")
    set = relationship("Set", back_populates="assigned")
    course = relationship("Course", back_populates="assigned")
    student = relationship("User", back_populates="assigned_exams")

