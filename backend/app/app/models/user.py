# from sqlalchemy import  Column, Integer, String, Date, DateTime
# from sqlalchemy.orm import relationship
# from app.db.base_class import Base
# from sqlalchemy.dialects.mysql import TINYINT

# class User(Base):
#     __tablename__ = "user"

#     id = Column(Integer,primary_key=True,index=True)
#     name = Column(String(50))
#     dob = Column(Date)
#     address = Column(String(100))
#     user_type = Column(TINYINT,comment="1-> Admin, 2-> Trainer, 3-> Student")

#     created_at = Column(DateTime)
#     updated_at = Column(DateTime)

#     # relationship
#     student_enroled_courses = relationship("StudentCourseEnrolment",back_populates="student")
#     trainer = relationship("TrainerEnrolment", back_populates="trainer")

