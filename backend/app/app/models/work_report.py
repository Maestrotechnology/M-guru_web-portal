from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey,Text,DECIMAL
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class WorkReport(Base):
    __tablename__ = "work_report"

    id = Column(Integer,primary_key=True,index=True)
    trainer_id = Column(Integer,ForeignKey("user.id"))
    date=Column(DateTime)
    batch_id=Column(Integer,ForeignKey("batch.id"))
    description=Column(String(350))
    taken_time=Column(DateTime)
    status = Column(TINYINT, comment="1-> active 2 -> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    batch = relationship("Batch",back_populates="work_report")
    user = relationship("User",back_populates="work_report")





