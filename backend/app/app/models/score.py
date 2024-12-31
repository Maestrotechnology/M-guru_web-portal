from sqlalchemy.orm import relationship
from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class Score(Base):
    __tablename__ = "score"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(100))
    status = Column(TINYINT, comment="1-> active 2 -> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    mark = Column(Integer)
    # ForeignKey
    created_by = Column(Integer, ForeignKey('user.id'))
    task_id = Column(Integer, ForeignKey("task.id"))
    student_id = Column(Integer, ForeignKey("user.id"))
    teacher_id = Column(Integer, ForeignKey("user.id"))
    student_project_id = Column(Integer, ForeignKey("student_project_detail.id"))

    # relationship
    project_detail = relationship("StudentProjectDetail", back_populates="score")
    task = relationship("Task", back_populates="scores")
    student = relationship("User", foreign_keys=[student_id], back_populates="scores_as_student")
    teacher = relationship("User", foreign_keys=[teacher_id], back_populates="scores_as_teacher")
    creator_user = relationship("User", foreign_keys=[created_by], back_populates="creator")  # Renamed `creator` to `score_creator`
