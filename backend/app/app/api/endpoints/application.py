from fastapi import APIRouter,Depends,UploadFile
from typing import Annotated
from api.deps import get_db

router = APIRouter()