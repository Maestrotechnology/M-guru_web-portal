# from sqlalchemy import  Column, Integer, String, DateTime
# from sqlalchemy.orm import relationship
# from app.db.base_class import Base
# from sqlalchemy.dialects.mysql import TINYINT


# class Batch(Base):
#     __tablename__ = "batch"

#     id = Column(Integer,primary_key=True,index=True)
#     name = Column(String(50))
#     description = Column(String(50))
#     status = Column(TINYINT, comment="1-> active , 2-> delete")
    
#     created_at = Column(DateTime)
#     updated_at = Column(DateTime)

#     # relationship
#     student_enroled_courses = relationship("StudentCourseEnrolment",back_populates="batch")
