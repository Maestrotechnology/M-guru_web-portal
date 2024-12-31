# app/models/course_assign.py

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class CourseAssign(Base):
    __tablename__ = "course_assign"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    course_id = Column(Integer, ForeignKey('course.id'))
    created_by = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    status = Column(TINYINT(1), comment='1->active 2-> inactive')

    # Relationships
    user = relationship(
        "User",
        foreign_keys=[user_id],  # Specify the foreign key
        back_populates="courses_assigned"
    )
    created_by_user = relationship(
        "User",
        foreign_keys=[created_by],  # Specify the foreign key
        back_populates="created_courses_assignments"
    )
    course = relationship("Course", back_populates="course_assignments")
