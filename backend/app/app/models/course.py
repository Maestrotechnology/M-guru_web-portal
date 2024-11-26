# from sqlalchemy import  Column, Integer, String, DateTime
# from sqlalchemy.orm import relationship
# from app.db.base_class import Base
# from sqlalchemy.dialects.mysql import TINYINT


# class Course(Base):
#     __tablename__ = "course"

#     id = Column(Integer, primary_key=True,index=True)
#     name = Column(String(50))
#     status = Column(TINYINT, comment="1-> active , 2-> inactive")
#     created_at = Column(DateTime)
#     updated_at = Column(DateTime)

#     # relationship
#     enrolments = relationship("StudentCourseEnrolment", back_populates="course")