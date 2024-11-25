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
    is_active = Column(TINYINT,comment = "1->active,2->inactive,0->delete")
    reset_key=Column(String(255))
    otp = Column(String(10))
    otp_expire_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

     # Relationships
    enrolled_batches_details = relationship(
        "BatchCourseDetails",
        foreign_keys="[BatchCourseDetails.student_id]",
        back_populates="student",
    )
    assigned_batches_details = relationship(
        "BatchCourseDetails",
        foreign_keys="[BatchCourseDetails.trainer_id]",
        back_populates="trainer",
    )



