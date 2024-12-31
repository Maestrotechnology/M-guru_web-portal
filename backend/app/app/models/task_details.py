from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey,Text,DECIMAL,Time
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT


class TaskDetail(Base):
    __tablename__ = "task_detail"
    id = Column(Integer,primary_key=True,index=True)
    attendance_id =Column(Integer,ForeignKey("attendance.id"))
    task =Column(String(350))
    student_id=Column(Integer,ForeignKey("user.id"))
    expected_time=Column(Time)
    mentor_time=Column(Time)
    trainer_id=Column(Integer,ForeignKey("user.id"))
    rating=Column(Integer)
    close_status=Column(TINYINT, comment="1-> close ")
    complete_status = Column(TINYINT, comment="1-> complete  ")
    task_description = Column(Text)
    mentor_description = Column(Text)
    status = Column(TINYINT, comment="1-> active 2 -> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    created_by = Column(Integer,ForeignKey('user.id'))

    attendance = relationship("Attendance",back_populates="task_detail")
    student = relationship("User",foreign_keys=[student_id],back_populates="student_task_detail")
    trainer = relationship("User",foreign_keys=[trainer_id],back_populates="trainer_task_details")
    # work_history = relationship("WorkHistory",back_populates="task_detail")
    creator = relationship("User",foreign_keys=[created_by],back_populates="task_creator")