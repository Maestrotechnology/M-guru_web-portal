from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class AssignExam(Base):
    __tablename__ = "assign_exam"

    id = Column(Integer, primary_key=True, index=True)

    status = Column(TINYINT, comment="1-> active , 2-> inactive")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    assigned_by = Column(Integer, ForeignKey('user.id'))
    batch_id = Column(Integer, ForeignKey("batch.id"), index=True)
    exam_id = Column(Integer, ForeignKey("exam.id"), index=True)
    set_id = Column(Integer, ForeignKey("question_set.id"), index=True)
    course_id = Column(Integer, ForeignKey("course.id"), index=True)
    student_id = Column(Integer, ForeignKey("user.id"), index=True)

    # relationships
    batch = relationship("Batch", back_populates="assigned_exams")
    exam = relationship("Exam", back_populates="assigned")
    question_set = relationship("QuestionSet", back_populates="assigned")
    course = relationship("Course", back_populates="assigned")
    
    # Specify the foreign keys explicitly
    student = relationship("User", foreign_keys=[student_id], back_populates="student_assigned_exams")
    assigner = relationship("User", foreign_keys=[assigned_by], back_populates="trainer_assigner")

    exam_details = relationship("StudentExamDetail", back_populates="assigned")
    assigned_question = relationship("AssignedQuestion",back_populates="assign_exam")
    