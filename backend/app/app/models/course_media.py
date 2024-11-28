from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey,Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT


class CourseMedia(Base):
    __tablename__ = "course_media"

    id = Column(Integer,primary_key=True,index=True)
    file_url = Column(Text)
    status = Column(TINYINT, comment="1-> active 2 -> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    # ForeignKey
    course_material_id = Column(Integer,ForeignKey("course_material.id"))

    # relationship
    course_material = relationship("CourseMaterial",back_populates="documents")