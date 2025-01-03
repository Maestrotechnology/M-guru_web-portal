from sqlalchemy.orm import relationship
from sqlalchemy import  Column, Integer, String, DateTime, ForeignKey
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class Option(Base):
    __tablename__ = "option"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    answer_status = Column(TINYINT, comment="1->correct answer")

    status = Column(TINYINT, comment="1-> active , 2-> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # ForeignKey
    created_by = Column(Integer,ForeignKey("user.id"))
    question_id = Column(Integer, ForeignKey("question.id"),index=True)

    # relationship
    question = relationship("Question", back_populates="options")
    user = relationship("User", back_populates="options") 