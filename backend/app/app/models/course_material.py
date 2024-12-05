from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey,Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class CourseMaterial(Base):
    __tablename__ = "course_material"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(25))
    description = Column(Text)
    status = Column(TINYINT, comment="1-> active 2 -> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # ForeignKey
    batch_id = Column(Integer,ForeignKey("batch.id"))
    course_id = Column(Integer,ForeignKey("course.id"))
    created_by_user_id = Column(Integer, ForeignKey("user.id"))

    #relationship
    course = relationship("Course",back_populates="materials")
    documents = relationship("CourseMedia", back_populates="course_material")
    created_by = relationship("User",back_populates="materials")
    batch = relationship("Batch",back_populates="course_material")
