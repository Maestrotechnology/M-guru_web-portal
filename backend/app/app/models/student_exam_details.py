from sqlalchemy.orm import relationship
from sqlalchemy import  Column, Integer, String, Text ,DateTime, ForeignKey
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class StudentExamDetail(Base):
    __tablename__ = "student_exam_detail"

    id = Column(Integer, index=True, primary_key=True)
    option_ids = Column(String(50))
    answer = Column(Text)
    mark = Column(Integer)
    
    status = Column(TINYINT, comment="1-> active , 2-> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    created_by = Column(Integer, ForeignKey('user.id'))
    type__id = Column(Integer, ForeignKey("type_of_question.id"), index=True)
    assign_exam_id = Column(Integer, ForeignKey("assign_exam.id"),index=True)
    student_id = Column(Integer, ForeignKey("user.id"), index=True)
    question_id = Column(Integer, ForeignKey("question.id"), index=True)


    assigned = relationship("AssignExam", back_populates="exam_details")
    student = relationship("User",foreign_keys=[student_id], back_populates="exam_details")
    user = relationship('User', foreign_keys=[created_by],back_populates='student_exam_detail')
    question = relationship("Question", back_populates="exam_details")
    type_of = relationship("TypeOfQuestion", back_populates="exam_details")