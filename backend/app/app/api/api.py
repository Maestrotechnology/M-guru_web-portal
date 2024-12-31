from fastapi import APIRouter
from .endpoints import (login,
                        application,
                        batch,
                        course,
                        enquiryType,
                        dropdown,
                        login,
                        user,
                        course_material,
                        checkin,
                        task,
                        score,
                        student_project_details,
                        dashboard,
                        question,
                        exam,
                        set
                        )

api_router = APIRouter()

api_router.include_router(login.router,tags=["Login"])
api_router.include_router(application.router, tags=["Application"],prefix='/application')
api_router.include_router(batch.router,tags=["Batch"],prefix='/batch')
api_router.include_router(course.router,tags=["Course"],prefix='/course')
api_router.include_router(enquiryType.router,tags=["EnquiryType"],prefix='/enquiry_type')
api_router.include_router(dropdown.router,tags=["Dropdown"],prefix='/drop_down')
api_router.include_router(user.router,tags=["User"],prefix='/user')
api_router.include_router(course_material.router,tags=["Course Material"],prefix='/course_material')
api_router.include_router(checkin.router,tags=["Checkin"],prefix='/erp')
api_router.include_router(task.router,tags=["Task"],prefix='/task')
api_router.include_router(score.router,tags=["Score"],prefix='/score')
api_router.include_router(student_project_details.router,tags=["Student Project details"],prefix='/student_project_details')
api_router.include_router(dashboard.router,tags=["Dashboard"],prefix='/dashboard')
api_router.include_router(question.router, tags=["Question"],prefix='/question')
api_router.include_router(exam.router, tags=["Exam"],prefix='/exam')
api_router.include_router(set.router, tags=["Set"],prefix='/set')


