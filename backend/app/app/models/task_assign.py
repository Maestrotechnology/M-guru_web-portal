from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey,Text,DECIMAL,Time
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT


class TaskAssign(Base):
    __tablename__ = "task_assign"
    id = Column(Integer,primary_key=True,index=True)
    task_id = Column(Integer,ForeignKey("task.id"))
    batch_id = Column(Integer,ForeignKey("batch.id"))
    created_by = Column(Integer,ForeignKey("user.id"))
    created_at = Column(DateTime)
    update_at = Column(DateTime)
    status = Column(TINYINT(1),comment="1=active -1=inactive")

    user = relationship("User",back_populates="task_assign")
    batch = relationship("Batch",back_populates="task_assign")
    task = relationship("Task",back_populates="task_assign")