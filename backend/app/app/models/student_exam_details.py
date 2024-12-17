from sqlalchemy.orm import relationship
from sqlalchemy import  Column, Integer, String, Text ,DateTime, ForeignKey
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class StudentExamDetail(Base):
    __tablename__ = "student_exam_detail"

    id = Column(Integer, index=True, primary_key=True)
    option_ids = Column(String(50))
    answer = Column(Text)

    status = Column(TINYINT, comment="1-> active , 2-> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    assign_exam_id = Column(Integer, ForeignKey("assign_exam.id"),index=True)
    student_id = Column(Integer, ForeignKey("user.id"), index=True)
    question_id = Column(Integer, ForeignKey("question.id"), index=True)

    assigned = relationship("AssignExam", back_populates="exam_details")
    student = relationship("User", back_populates="exam_details")
    question = relationship("Question", back_populates="exam_details")
    