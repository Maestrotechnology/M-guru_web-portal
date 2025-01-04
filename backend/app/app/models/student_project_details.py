from sqlalchemy.orm import relationship
from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class StudentProjectDetail(Base):
    __tablename__ = "student_project_detail"

    id = Column(Integer,primary_key=True,index=True)
    mark = Column(Integer)
    project_url = Column(String(255))
    project_start_date = Column(DateTime)
    project_end_date = Column(DateTime)
    description = Column(String(255))

    status = Column(TINYINT, comment="1-> active 2 -> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_marked = Column(TINYINT(1),comment="1-> marked 0-> didn't marked")
    # ForeignKey
    created_by = Column(Integer,ForeignKey('user.id'))
    task_id = Column(Integer,ForeignKey("task.id"))
    student_id = Column(Integer,ForeignKey("user.id"))

    # relationship
    score = relationship("Score", back_populates="project_detail")
    task = relationship("Task", back_populates="project_details")
    student = relationship("User",foreign_keys=[student_id],back_populates="project_details")
    user = relationship("User", foreign_keys=[created_by], back_populates="project_creator")