from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey,Text,DECIMAL,Time
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
    taken_time=Column(Time)
    status = Column(TINYINT, comment="1-> active 2 -> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey('user.id'))
    batch = relationship("Batch",back_populates="work_report")
    trainer = relationship("User",foreign_keys=[trainer_id],back_populates="trainer_work_report")
    creator = relationship("User",foreign_keys=[created_by],back_populates='creator_work_report')