from sqlalchemy.orm import relationship
from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class Interview(Base):
    __tablename__ = "interview"

    id = Column(Integer, primary_key=True, index=True)
    scheduled_date = Column(DateTime)
    attended_date = Column(DateTime)
    communication_mark =Column(Integer)
    aptitude_mark = Column(Integer)
    programming_mark = Column(Integer)
    overall_mark = Column(Integer)

    status = Column(TINYINT, comment="1-> active 2 -> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)    
    # ForeignKey
    created_by = Column(Integer,ForeignKey('user.id'))
    application_id = Column(Integer, ForeignKey("application_details.id"))

    # relationship
    application = relationship("ApplicationDetails", back_populates="interview_details")
    user = relationship('User', back_populates='interview')