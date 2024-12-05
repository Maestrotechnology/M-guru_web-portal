from sqlalchemy.orm import relationship
from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(50))
    task_report_url = Column(String(255))
    from_date = Column(DateTime)
    end_date = Column(DateTime)
    description = Column(String(250))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    status = Column(TINYINT, comment="1-> active , 2-> inactive")
    # ForeignKey
    course_id = Column(Integer, ForeignKey("course.id"))
    batch_id = Column(Integer, ForeignKey("batch.id"))
    created_by_user_id = Column(Integer, ForeignKey("user.id"))
    # relationship
    course = relationship("Course",back_populates="task")
    batch = relationship("Batch",back_populates="task")
    created_by = relationship("User",back_populates="created_task")
    attendance = relationship("Attendance",back_populates="task")
   
    scores = relationship("Score",back_populates="task")
    project_details = relationship("StudentProjectDetail", back_populates="task")