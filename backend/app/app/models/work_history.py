from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey,Text,DECIMAL
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT


class WorkHistory(Base):
    __tablename__ = "work_history"

    id = Column(Integer,primary_key=True,index=True)
    work_report_id = Column(Integer,ForeignKey("work_report.id"))
    break_time=Column(DateTime)
    work_time=Column(DateTime)
    status = Column(TINYINT, comment="1-> active 2 -> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    work_report = relationship("WorkReport",back_populates="work_history",uselist=False)
    
    