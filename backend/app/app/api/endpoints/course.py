from fastapi import APIRouter, Depends, Form
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

@router.post("/create_cource")
async def createCource(db:Session=Depends(get_db),
                     token:str = Form(...),
                     name:str = Form(...)):
    
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    get_cource=db.query(Course).filter(Course.status==1,Course.name==name).first()
    if  get_cource:
        return {"status":0,"msg":"Course  Name Already exit"}
    addCource =  Course(
                    name=name,
                    created_at = datetime.now(),
                    status =1,
                    )
    db.add(addCource)
    db.commit()
    return {
        "status" : 1,
        "msg":"Course created successfully"
    }

@router.post("/update_course")
async def updateCourse(db:Session=Depends(get_db),
                     token:str = Form(...),
                     course_id:int = Form(...),
                     name:str = Form(None),
                     ):
    
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    check_course=db.query(Course).filter(Course.status==1)
    get_course=check_course.query(Course).filter(Course.id==course_id).first()
    if not get_course:
        return {"status":0,"msg":"Course Id not found"}
    if name:
        if check_course.filter(Course.id!=course_id,Course.name==name).first():
            return {"status":0,"msg":"Course Name is already exist"}

    get_course.name=name
    get_course.updated_at=datetime.now()
    db.commit()
    return {
        "status" : 1,
        "msg":"Course Updated successfully"
    }

@router.post("/delete_Course")
async def deleteCourse(db:Session=Depends(get_db),
                     token:str = Form(...),
                     Course_id:int = Form(...) ):
    
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    get_Course=db.query(Course).filter(Course.id==Course_id,Course.status==1).first()
    if not get_Course:
        return {"status":0,"msg":"Course Id not found"}
    get_Course.status=-1
    db.commit()
    return {
        "status" : 1,
        "msg":"Course deleted successfully"
    }

@router.post("/list_Course")
async def listCourse(
                    db:Session=Depends(deps.get_db),
                   token:str=Form(...),page:int=1,
                   size:int=10,
                   Course_name:str=Form(None),
):
    user=get_user_token(db=db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    getCourse =  db.query(Course).filter(Course.status ==1)
    
    
    if Course_name:
           getCourse = getCourse.filter(Course.name.like("%"+Course_name+"%"))
    if user.user_type == 3:
        getCourse = getCourse.filter(Course.id == user.course_id)
        
    getCourse = getCourse.order_by(Course.name)
    totalCount= getCourse.count()
    total_page,offset,limit=get_pagination(totalCount,page,size)
    getCourse=getCourse.limit(limit).offset(offset).all()
    dataList =[]

    for row in getCourse:
            dataList.append({
                "course_id" :row.id,
                "course_name":row.name,
                "created_at":row.created_at,
            
            })
    data=({"page":page,"size":size,"total_page":total_page,
                "total_count":totalCount,
                "items":dataList})
    return {"status":1,"msg":"Success","data":data}
    
    







