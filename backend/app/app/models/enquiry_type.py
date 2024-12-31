from sqlalchemy.orm import relationship
from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class EnquiryType(Base):
    __tablename__ = "enquiry_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    status = Column(TINYINT, comment="1-> active , 2-> inactive")
    created_at = Column(DateTime)
    created_by = Column(Integer,ForeignKey('user.id'))
    updated_at = Column(DateTime)
    # relationship
    applications = relationship("ApplicationDetails", back_populates="enquires")
    user = relationship('User', back_populates='enquiry_type')