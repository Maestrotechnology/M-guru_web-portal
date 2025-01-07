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
        filter(Course.status==1).order_by(Course.name.asc())
        if user.user_type ==2:
            getAllCourse = getAllCourse.join(CourseAssign,Course.id==CourseAssign.course_id).filter(CourseAssign.user_id==user.id,CourseAssign.status==1).distinct(Course.id)
        getAllCourse = getAllCourse.all()
        dataList = []
        if getAllCourse:
            for row in getAllCourse:
                dataList.append({
                    "Course_Id":row.id,
                    "Course_name":row.name.capitalize()
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
                    "Batch_name":row.name.capitalize()
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
                    "EnquiryType_name":row.name.capitalize()
                })
        return {"status":1,"msg":"Success","data":dataList}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login later."}
    
@router.post("/dropDownTask")
async def dropDownTask(
                        db:Session = Depends(deps.get_db),
                        token:str=Form(...),
                        course_id : int=Form(None),
):
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    get_task = db.query(Task).filter(Task.status == 1).order_by(Task.name)
    if user.user_type ==2:
        get_task = get_task.join(CourseAssign,CourseAssign.course_id==Task.course_id).filter(CourseAssign.user_id==user.id,CourseAssign.status==1)
    if user.user_type ==3:
        get_task = get_task.join(CourseAssign,CourseAssign.course_id==Task.course_id
                    ).join(TaskAssign,Task.id==TaskAssign.task_id).filter(CourseAssign.user_id==user.id,
                    CourseAssign.status==1,TaskAssign.batch_id==user.batch_id,TaskAssign.status==1)
    if course_id:
        get_task = get_task.filter(Task.course_id == course_id)
    get_task = get_task.all()
    data_list = []
    for data in get_task:
        data_list.append({
            "id":data.id,
            "name":data.name,
        })
    return {"status":1,"msg":"Success","data":data_list}


@router.post("/dropDownTrainer")
async def dropDownTrainer(
                        db:Session = Depends(deps.get_db),
                        token:str=Form(...)
):
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    get_user = db.query(User).filter(User.status == 1,User.user_type==2).order_by(User.name).all()
    data_list = []
    for data in get_user:
        data_list.append({
            "id":data.id,
            "name":data.name.capitalize()
        })
    return {"status":1,"msg":"Success","data":data_list}


# @router.post("/dropdown_year")
# async def dropdownYear(
#                         db:Session = Depends(deps.get_db),
#                         token:str=Form(...)
# ):
#     user = get_user_token(db,token=token)
#     if not user:
#         return {"status":0,"msg":"Your login session expires.Please login again."}
    
#     get_year = db.query(PassoutYear).all()
#     data_list = []
#     for data in get_year:
#         data_list.append({
#             "id":data.id,
#             "name":data.name
#         })
#     return {"status":1,"msg":"Success","data":data_list}

@router.post("/downQuestionType")
async def questionType(
                        db: Session = Depends(get_db),
                        token: str = Form(...)
):
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    get_question_type = db.query(TypeOfQuestion).filter(TypeOfQuestion.status == 1).all()
    data_list = []
    for data in get_question_type:
        data_list.append({
            "id":data.id,
            "name":data.name.capitalize()
        })
    return {"status":1,"msg":"Success","data":data_list}

@router.post("/dropdown_active_batch_student")
async def dropdownActiveBatchStudent(
                                        db: Session = Depends(get_db),
                                        token: str = Form(...),
                                        course_id : int = Form(None),
                                        batch_id : int = Form(None),
):
        user = get_user_token(db,token=token)
        if not user:
            return {"status":0,"msg":"Your login session expires.Please login again."}
        
        get_students = db.query(User).join(Batch,
                          Batch.id == User.batch_id                   
                        ).join(CourseAssign,CourseAssign.user_id==User.id).filter(User.user_type == 3, User.status == 1, Batch.status == 1,CourseAssign.status==1).order_by(User.name)
        if course_id:
            get_students = get_students.filter(CourseAssign.course_id == course_id)
        if batch_id:
            get_students = get_students.filter(User.batch_id==batch_id)
        get_students = get_students.all()
        data_list = []
        for data in get_students:
            data_list.append({
                "id":data.id,
                "name":data.name.capitalize()
            })
        return {"status":1,"msg":"Success","data":data_list}

@router.post("/dropdown_exam")
async def dropDownExam(
                         db: Session = Depends(get_db),
                         token: str = Form(...),
                         course_id : int = Form(None),
):
        user = get_user_token(db,token=token)
        if not user:
            return {"status":0,"msg":"Your login session expires.Please login again."}
        
        get_exam = db.query(Exam).filter(Exam.status == 1)
        if course_id:
            get_exam = get_exam.filter(Exam.course_id==course_id)
        get_exam = get_exam.all()
        data_list = []
        for data in get_exam:
            data_list.append({
                "id":data.id,
                "name":data.name.capitalize()
            })
        return {"status":1,"msg":"Success","data":data_list}

