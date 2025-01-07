from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship,backref
from app.db.base_class import Base
from sqlalchemy.dialects.mysql import TINYINT

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    email = Column(String(100), index=True)
    phone = Column(String(50))
    user_type = Column(TINYINT, comment="1-> Admin, 2-> Trainer, 3-> Student")
    username = Column(String(100), index=True)
    password = Column(String(100))
    address = Column(Text)
    create_at = Column(DateTime)
    update_at = Column(DateTime)
    status = Column(TINYINT, comment="1->active,2->inactive,-1->delete")
    reset_key = Column(String(255))
    otp = Column(String(10))
    otp_expire_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey('user.id'), nullable=True)
    # ForeignKey
    batch_id = Column(Integer, ForeignKey("batch.id"))

    # Relationships
    user_creator = relationship("User", backref=backref("created_users", uselist=True), remote_side=[id])
    batch = relationship("Batch", back_populates="users", foreign_keys=[batch_id])  # Batch can be one-to-one
    created_batches = relationship("Batch", foreign_keys="[Batch.created_by]", back_populates="creator")
    course_material = relationship("CourseMaterial", back_populates="user")
    attendance = relationship("Attendance", back_populates="users")
    task = relationship("Task", back_populates="user")
    
    # Renamed `creator` to `score_creator` to avoid conflict
    creator = relationship("Score", foreign_keys="[Score.created_by]", back_populates="creator_user")
    
    scores_as_student = relationship("Score", foreign_keys="[Score.student_id]", back_populates="student")
    scores_as_teacher = relationship("Score", foreign_keys="[Score.teacher_id]", back_populates="teacher")
    project_details = relationship("StudentProjectDetail", foreign_keys="[StudentProjectDetail.student_id]", back_populates="student")
    
    # Renamed second `creator` to `project_creator` to avoid conflict
    project_creator = relationship("StudentProjectDetail", foreign_keys="[StudentProjectDetail.created_by]", back_populates="user")
    
    student_task_detail = relationship("TaskDetail", foreign_keys="[TaskDetail.student_id]", back_populates="student")
    trainer_task_details = relationship("TaskDetail", foreign_keys="[TaskDetail.trainer_id]", back_populates="trainer")
    task_creator = relationship("TaskDetail", foreign_keys="[TaskDetail.created_by]", back_populates="creator")

    api_tokens = relationship("ApiTokens", back_populates="user")
    trainer_work_report = relationship("WorkReport", foreign_keys="[WorkReport.trainer_id]", back_populates="trainer")
    creator_work_report = relationship("WorkReport", foreign_keys="[WorkReport.created_by]", back_populates="creator")
    
    # Assign exam relationships
    student_assigned_exams = relationship("AssignExam", foreign_keys="[AssignExam.student_id]", back_populates="student")
    trainer_assigner = relationship("AssignExam", foreign_keys="[AssignExam.assigned_by]", back_populates="assigner")
    
    exam_details = relationship("StudentExamDetail", foreign_keys="[StudentExamDetail.student_id]", back_populates="student")
    
    # Many-to-many relationship with Course through CourseAssign
    courses_assigned = relationship("CourseAssign", back_populates="user", foreign_keys="[CourseAssign.user_id]")
    created_courses_assignments = relationship("CourseAssign", back_populates="created_by_user", foreign_keys="[CourseAssign.created_by]")
    application_details = relationship('ApplicationDetails', back_populates='user')
    course_media = relationship("CourseMedia", back_populates="user")
    course = relationship("Course", back_populates="user")
    enquiry_type = relationship("EnquiryType", back_populates="user")
    exam = relationship("Exam", back_populates="user")
    interview = relationship("Interview", back_populates="user")
    material_access = relationship('MaterialAccess', back_populates='user')
    options = relationship('Option', back_populates='user')
    question = relationship('Question', back_populates='user')
    question_set = relationship('QuestionSet', back_populates='user')
    student_exam_detail = relationship('StudentExamDetail', foreign_keys='[StudentExamDetail.created_by]', back_populates='user')
    type_of_question = relationship('TypeOfQuestion', back_populates='user')
    task_assign = relationship("TaskAssign",back_populates="user")
    assigned_question = relationship("AssignedQuestion",back_populates="student")