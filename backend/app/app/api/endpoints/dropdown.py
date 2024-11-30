from fastapi import APIRouter, Depends, Form,UploadFile,File
from sqlalchemy.orm import Session
from app.models import ApiTokens,User
from app.api import deps
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime
from app.utils import *
from sqlalchemy import or_
from pydantic import EmailStr
from api.deps import get_db,authenticate,get_by_user,get_user_token,phoneNo_validation

router = APIRouter()

@router.post("/dropDownCourse")
async def dropDownCourse(db:Session = Depends(deps.get_db),
                           token:str=Form(...)):
    user = deps.get_user_token(db=db,token =token)
    if user:
        getAllCourse= db.query(Course).\
        filter(Course.status==1).order_by(Course.name.asc()).all()
        dataList = []
        if getAllCourse:
            for row in getAllCourse:
                dataList.append({
                    "Course_Id":row.id,
                    "Course_name":row.name
                })
        return {"status":1,"msg":"Success","data":dataList}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login later."}
    
@router.post("/dropDownBatch")
async def dropDownBatch(db:Session = Depends(deps.get_db),
                           token:str=Form(...)):
    user = deps.get_user_token(db=db,token =token)
    if user:
        getAllBatch= db.query(Batch).\
        filter(Batch.status==1).order_by(Batch.name.asc()).all()
        dataList = []
        if getAllBatch:
            for row in getAllBatch:
                dataList.append({
                    "Batch_Id":row.id,
                    "Batch_name":row.name
                })
        return {"status":1,"msg":"Success","data":dataList}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login later."}
    
@router.post("/dropDownEnquiry")
async def dropDownEnquiry(db:Session = Depends(deps.get_db),
                           token:str=Form(...)):
    user = deps.get_user_token(db=db,token =token)
    if user:
        getAllEnquiry= db.query(EnquiryType).\
        filter(EnquiryType.status==1).order_by(EnquiryType.name.asc()).all()
        dataList = []
        if getAllEnquiry:
            for row in getAllEnquiry:
                dataList.append({
                    "EnquiryType_Id":row.id,
                    "EnquiryType_name":row.name
                })
        return {"status":1,"msg":"Success","data":dataList}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login later."}
    
@router.post("/dropDownTask")
async def dropDownTask(
                        db:Session = Depends(deps.get_db),
                        token:str=Form(...)
):
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    get_task = db.query(Task).filter(Task.status == 1).order_by(Task.name).all()
    data_list = []
    for data in get_task:
        data_list.append({
            "id":data.id,
            "name":data.name
        })
    return {"status":1,"msg":"Success","data":data_list}
    