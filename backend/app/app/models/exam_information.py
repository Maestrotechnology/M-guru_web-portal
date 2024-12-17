from sqlalchemy.orm import relationship
from sqlalchemy import  Column, Integer, String, Text ,DateTime, ForeignKey
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class ExamInformarion(Base):
    __tablename__ = "exam_informarion"
    id = Column(Integer, index=True, primary_key=True)
    StudentExamDetail_id = Column(Integer, ForeignKey("student_exam_detail.id"))
    answer_id=Column(Integer,ForeignKey("option.id"))
    status = Column(TINYINT, comment="1-> active , 2-> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    option = relationship("Option", back_populates="exam_informarion")
    exam_details = relationship("StudentExamDetail", back_populates="exam_informarion")
    