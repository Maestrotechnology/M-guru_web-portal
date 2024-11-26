from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class BatchCourseDetails(Base):
    __tablename__ = "batch_course_details"

    id = Column(Integer,primary_key=True, index=True)
    status = Column(TINYINT, comment="1-> active 2 -> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    # ForeignKey
    batch_id = Column(Integer, ForeignKey("batch.id"))
    student_id = Column(Integer, ForeignKey("user.id"))
    course_id = Column(Integer, ForeignKey("course.id"))
    trainer_id = Column(Integer, ForeignKey("user.id"))

    # relationship
    batch = relationship("Batch", back_populates="batch_details")
    student = relationship("User", foreign_keys=[student_id], back_populates="enrolled_batches_details")
    course = relationship("Course", back_populates="batch_details")
    trainer = relationship("User", foreign_keys=[trainer_id], back_populates="assigned_batches_details")

