from fastapi import APIRouter
from .endpoints import login,application

api_router = APIRouter()

api_router.include_router(login.router,tags=["login"])
api_router.include_router(application.router, tags=["application"])