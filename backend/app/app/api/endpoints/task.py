# from fastapi import APIRouter,Depends,UploadFile,Form,File
# from typing import Annotated
# from api.deps import get_db
# from sqlalchemy.orm import Session
# from pydantic import EmailStr
# from app.models import Course,ApplicationDetails,EnquiryType,Interview
# from core.config import settings
# from datetime import datetime
# from utils import file_storage,send_mail,get_pagination


# router = APIRouter()

# @router.post("/create_task")
# async def createTask(
#                       db: Session = Depends(get_db),
#                       token: str = Form(...),
#                       name: str 
# ):