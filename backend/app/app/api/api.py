from fastapi import APIRouter
from .endpoints import login,application,batch,course,enquiryType,dropdown,login,user,course_material

api_router = APIRouter()

api_router.include_router(login.router,tags=["Login"])
api_router.include_router(application.router, tags=["Application"])
api_router.include_router(batch.router,tags=["Batch"])
api_router.include_router(course.router,tags=["Course"])
api_router.include_router(enquiryType.router,tags=["EnquiryType"])
api_router.include_router(dropdown.router,tags=["Dropdown"])
api_router.include_router(user.router,tags=["User"])
api_router.include_router(course_material.router,tags=["Course Material"])


