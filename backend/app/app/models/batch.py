from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class Batch(Base):
    __tablename__ = "batch"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    description = Column(String(350))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    fee = Column(Integer)
    status = Column(TINYINT, comment="1-> active , 2-> delete")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey("user.id"))

    # Relationships
    users = relationship("User", foreign_keys='[User.batch_id]', back_populates="batch")  # Many Users can belong to one Batch
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_batches", uselist=False) 
    applications = relationship("ApplicationDetails", back_populates="batch")
    # task = relationship("Task", back_populates="batch")
    course_material = relationship("CourseMaterial", back_populates="batch")
    work_report = relationship("WorkReport", back_populates="batch")
    assigned_exams = relationship("AssignExam", back_populates="batch")
    material_access = relationship("MaterialAccess", back_populates="batch")
    task_assign = relationship("TaskAssign",back_populates="batch")