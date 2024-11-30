from sqlalchemy import  Column, Integer, String, Date, DateTime,Text,ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    email = Column(String(100),index=True)
    phone = Column(String(50))
    user_type = Column(TINYINT,comment="1-> Admin, 2-> Trainer, 3-> Student")
    username = Column(String(100),index=True)
    password = Column(String(100))
    address = Column(Text)
    create_at = Column(DateTime)
    update_at = Column(DateTime)
    status = Column(TINYINT,comment = "1->active,2->inactive,0->delete")
    reset_key=Column(String(255))
    otp = Column(String(10))
    otp_expire_at = Column(DateTime)

    # ForeignKey
    batch_id = Column(Integer,ForeignKey("batch.id"))
    course_id = Column(Integer,ForeignKey("course.id"))


     # Relationships
    batch = relationship("Batch",back_populates="users",uselist=False)
    course = relationship("Course",back_populates="users",uselist=False)
    materials = relationship("CourseMaterial",back_populates="created_by")
    work_report = relationship("WorkReport", back_populates="users")
    created_task = relationship("Task",back_populates="created_by")
    # enrolled_batches_details = relationship(
    #     "BatchCourseDetails",
    #     uselist=False,
    #     foreign_keys="[BatchCourseDetails.student_id]",
    #     back_populates="student",
    # )
    # assigned_batches_details = relationship(
    #     "BatchCourseDetails",
    #     foreign_keys="[BatchCourseDetails.trainer_id]",
    #     back_populates="trainer",
    # )
    task_detail = relationship("TaskDetail",back_populates="user")
    api_tokens=relationship("ApiTokens",back_populates="user")


