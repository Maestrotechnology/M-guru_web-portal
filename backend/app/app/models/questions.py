from sqlalchemy.orm import relationship
from sqlalchemy import  Column, Integer, String, DateTime, ForeignKey
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True, index=True)
    question_title = Column(String(255))
    mark = Column(Integer)
    no_of_answers = Column(TINYINT)

    status = Column(TINYINT, comment="1-> active , 2-> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # ForeignKey
    question_type_id = Column(Integer, ForeignKey("type_of_question.id"), index=True)
    set_id = Column(Integer, ForeignKey("set.id"), index=True)
    exam_id = Column(Integer, ForeignKey("exam.id"), index= True)

    # relationship
    type_of = relationship("TypeOfQuestion",back_populates="questions")
    set = relationship("Set", back_populates="questions")
    exam = relationship("Exam", back_populates="questions")
    options = relationship("Options", back_populates="question")