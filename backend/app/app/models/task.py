from sqlalchemy.orm import relationship
from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(50))
    status = Column(TINYINT, comment="1-> active , 2-> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # ForeignKey
    created_by_user_id = Column(Integer, ForeignKey("user.id"))
    # relationship
    created_by = relationship("User",back_populates="created_task")
    work_report = relationship("WorkReport",back_populates="task")
    work_history = relationship("WorkHistory",back_populates="task")