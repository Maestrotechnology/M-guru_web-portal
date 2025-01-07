from sqlalchemy import  Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT

from app.db.base_class import Base

class AssignedQuestion(Base):
    __tablename__ = "assigned_question"
    id=Column(Integer,primary_key=True)
    assign_exam_id = Column(Integer,ForeignKey("assign_exam.id"))
    student_id = Column(Integer,ForeignKey("user.id"))
    question_id = Column(Integer,ForeignKey("question.id"))
    created_at = Column(DateTime)
    status = Column(TINYINT(1),comment="1->active 2->inactive")

    assign_exam = relationship("AssignExam",back_populates="assigned_question")
    student = relationship("User",back_populates="assigned_question")
    question = relationship("Question",back_populates="assigned_question")
    