# from sqlalchemy import  Column, Integer, String, Date, DateTime,ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.dialects.mysql import TINYINT
# from app.db.base_class import Base

# class TrainerEnrolment(Base):
#     __tablename__ = "trainer_enrolment"

#     id = Column(Integer, primary_key=True, index=True)
#     status = Column(TINYINT, comment="1-> active 2 -> inactive")
#     created_at = Column(DateTime)
#     updated_at = Column(DateTime)

#     # ForeignKey
#     trainer_id = Column(Integer, ForeignKey("user.id"))
#     course_id = Column(Integer, ForeignKey("course.id"))
#     batch_id = Column(Integer, ForeignKey("batch.id"))

#     # relationship
#     trainer = relationship("User", back_populates="trainer")



