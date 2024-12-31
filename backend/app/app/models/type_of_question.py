from sqlalchemy.orm import relationship
from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class TypeOfQuestion(Base):
    __tablename__ = "type_of_question"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

    status = Column(TINYINT, comment="1-> active , 2-> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    created_by = Column(Integer,ForeignKey('user.id'))
    # relationship
    questions = relationship("Question", back_populates="type_of")
    exam_details = relationship("StudentExamDetail", back_populates="type_of")
    user = relationship("User",back_populates='type_of_question')