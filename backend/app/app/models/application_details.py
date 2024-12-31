from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class ApplicationDetails(Base):
    __tablename__ = "application_details"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(50))
    phone = Column(String(20))
    resume = Column(String(255))
    qualification = Column(String(100))
    application_status = Column(TINYINT , comment="1-> seleted, 2-> rejected, null-> not defined")
    scholarship = Column(Integer)
    passed_out_year = Column(String(4))

    status = Column(TINYINT, comment="1-> active 2 -> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    # ForeignKey
    created_by = Column(Integer, ForeignKey('user.id'))
    enquiry_id = Column(Integer, ForeignKey("enquiry_type.id"))
    course_id = Column(Integer, ForeignKey("course.id"))
    batch_id = Column(Integer, ForeignKey("batch.id"))

    #relationship
    enquires = relationship("EnquiryType", back_populates="applications")
    courses = relationship("Course", back_populates="applications")
    interview_details = relationship("Interview", back_populates="application",uselist=False)
    batch = relationship("Batch",back_populates="applications",uselist=False)
    user = relationship('User',back_populates='application_details')