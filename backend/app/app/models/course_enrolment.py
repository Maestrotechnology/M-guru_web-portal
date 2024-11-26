# from sqlalchemy import  Column, Integer, String, DateTime,ForeignKey
# from sqlalchemy.orm import relationship
# from app.db.base_class import Base
# from sqlalchemy.dialects.mysql import TINYINT


# class StudentCourseEnrolment(Base):
#     __tablename__ = "student_course_enrolment"

#     id = Column(Integer,primary_key=True,index=True)
#     status = Column(TINYINT, comment="1-> active 2 -> inactive")
#     created_at = Column(DateTime)
#     updated_at = Column(DateTime)

#     # ForeignKey
#     course_id = Column(Integer, ForeignKey("course.id"))
#     student_id = Column(Integer, ForeignKey("user.id"))
#     batch_id = Column(Integer, ForeignKey("batch.id"))
    
#     # relationship
#     course = relationship("Course", back_populates="enrolments")
#     student = relationship("User", back_populates="student_enroled_courses")
#     batch = relationship("Batch", back_populates="student_enroled_courses")


