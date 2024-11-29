from fastapi import APIRouter
from .endpoints import login,application,batch,course,enquiryType,dropdown,login,user,checkin

api_router = APIRouter()

api_router.include_router(login.router,tags=["login"])
api_router.include_router(application.router, tags=["application"])
api_router.include_router(batch.router,tags=["batch"])
api_router.include_router(course.router,tags=["course"])
api_router.include_router(enquiryType.router,tags=["enquiryType"])
api_router.include_router(dropdown.router,tags=["dropdown"])
api_router.include_router(user.router,tags=["user"])
api_router.include_router(checkin.router,tags=["checkin"])



