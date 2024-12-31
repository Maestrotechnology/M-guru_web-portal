from sqlalchemy.orm import relationship
from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class Exam(Base):
    __tablename__ = "exam"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

    status = Column(TINYINT, comment="1-> active , 2-> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    created_by = Column(Integer,ForeignKey('user.id'))
    course_id = Column(Integer,ForeignKey("course.id"))
    # relationship
    course = relationship("Course",back_populates="exam")
    question_set = relationship("QuestionSet",back_populates="exam")
    questions = relationship("Question", back_populates="exam")
    assigned = relationship("AssignExam", back_populates="exam")
    user = relationship("User", back_populates="exam")
