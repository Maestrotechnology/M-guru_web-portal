from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey,Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class MaterialAccess(Base):
    __tablename__ = "material_access"

    id = Column(Integer,primary_key=True,index=True)
    batch_id = Column(Integer,ForeignKey('batch.id'))
    # course_id = Column(Integer,ForeignKey('course.id'))
    course_material_id = Column(Integer,ForeignKey('course_material.id'))
    created_by = Column(Integer,ForeignKey('user.id'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    status = Column(TINYINT(1),comment='1-> active 2-> inactive -1 -> deleted')

    batch = relationship('Batch',back_populates='material_access')
    # course = relationship("Course",back_populates="material_access")
    course_material =relationship('CourseMaterial',back_populates='material_access')
    user  =relationship('User',back_populates='material_access')