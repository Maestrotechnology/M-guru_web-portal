from sqlalchemy.orm import relationship
from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class Set(Base):
    __tablename__ = "set"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

    status = Column(TINYINT, comment="1-> active , 2-> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # ForeignKey
    exam_id = Column(Integer,ForeignKey("exam.id"),index=True)

    # relationship
    exam = relationship("Exam",back_populates="sets")
    questions = relationship("Question", back_populates="set")
    assigned = relationship("AssignExam", back_populates="set")