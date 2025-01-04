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
from api.deps import get_db,authenticate,get_by_user,get_user_token,phoneNo_validation,get_username

router = APIRouter()

@router.post("/create_user")
async def createUser(db:Session=Depends(get_db),
                     token:str = Form(...),
                     name:str = Form(...),
                     user_type:int=Form(...,description=("1->admin,2>Trainer, 3>Student")),
                     email:EmailStr=Form(...),
                     phone:str=Form(...),
                     address:str=Form(None),
                     password:str=Form(...),
                     course_id:str=Form(None,description='if multiple 1,2,3,4,5'),
                     batch_id:int=Form(None)
                     
):
    print(course_id)

        
    hashPassword = get_password_hash(password)
    
    user = get_user_token(db,token=token)
    
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}

    if user_type in [2,3]:
        if not course_id:
            return {"status":0,"msg":"Course required"}
    # if user_type == 3 and batch_id is None:
    #     return {"status":0,"msg":"Batch required for student"}
    checkUser = db.query(User).filter(User.status==1)

    if checkUser.filter(User.email == email).first():
        return {"status":0,"msg":"Given Email is already exist"}
    if checkUser.filter(User.phone==phone).first():
        return {"status":0,"msg":"Given Phone Number is already exist"}
    
    addUser =  User(
                    name=name,
                    username = get_username(db,user_type),
                    user_type=user_type,
                    email=email,
                    phone=phone,
                    password=hashPassword,
                    create_at = datetime.now(settings.tz_IN),
                    status =1,
                    address=address,
                    batch_id=batch_id,
                    # course_id=course_id
                    )
    db.add(addUser)
    db.commit()
    print(course_id)
    if course_id:
        course_ids = course_id.split(',')
        for course in course_ids:
            print(course)
            add_course = CourseAssign(
                user_id = addUser.id,
                course_id = course,
                created_by = user.id,
                created_at = datetime.now(settings.tz_IN),
                status = 1
            )
            db.add(add_course)
            db.commit()
    return {
        "status" : 1,
        "msg":"User created successfully"
    }

@router.post("/update_user")
async def updateUser(
                     db:Session=Depends(get_db),
                     token:str=Form(...),
                     name:str = Form(...),
                     userId:int=Form(...),
                     email:EmailStr=Form(...),
                     phone:str=Form(...),
                     address:str=Form(None),
                     course_id:str=Form(None,description='if multiple 1,2,3'),
                     ):
    
    user  = get_user_token(db,token=token)

    if not user:
        return {"status":0,"msg":"Account details not found"}
    
    checkUser = db.query(User).filter(User.status==1)

    getUser = checkUser.filter(User.id == userId,User.status==1).first()

    if not getUser:
        return {"status":0,"msg":"Given user id  not found"}
        
    # if getUser.user_type == 3 and not course_id:
    #     return {"status":0, "msg": "course is required"}

    # if username:
    #     if checkUser.filter(User.username == username,User.id!=userId).first():
    #         return {"status":0,"msg":"Given userName is already exist"}
    #     getUser.username = username
    if email:
        if checkUser.filter(User.email == email,User.id!=userId).first():
            return {"status":0,"msg":"Given Email is already exist"}
    if phone:
        if checkUser.filter(User.phone==phone,User.id!=userId).first():
            return {"status":0,"msg":"Given Phone Number is already exist"}
    getUser.email = email
    getUser.phone =  phone
    getUser.name=name
    getUser.address=address
    getUser.update_at=datetime.now()
    db.commit()
    if course_id:
        # Convert course_id to a list of integers (split the comma-separated string)
        course_ids = [int(course) for course in course_id.split(",")]

        # Get all course assignments for the user
        assigned_courses = db.query(CourseAssign).filter(
            CourseAssign.user_id == userId
        ).all()

        # Create a set of course IDs the user should have access to
        # courses_to_assign = set(course_ids)

        # Handle each assigned course
        for course_assignment in assigned_courses:
            if course_assignment.course_id not in course_ids:
                # If the course is not in the new list, update its status to -1
                course_assignment.status = -1
                course_assignment.updated_at = datetime.now(settings.tz_IN)
                db.commit()
            else:
                # If the course is in the new list, ensure it's active
                if course_assignment.status != 1:
                    course_assignment.status = 1  # Reactivate course
                    course_assignment.updated_at = datetime.now(settings.tz_IN)
                    db.commit()

                # Remove it from the courses_to_assign set (it's already handled)
                course_ids.remove(course_assignment.course_id)

        # Add new courses that are not already assigned
        for new_course_id in course_ids:
            new_course_assign = CourseAssign(
                user_id=userId,
                course_id=new_course_id,
                created_by=user.id,
                created_at=datetime.now(settings.tz_IN),
                updated_at=datetime.now(settings.tz_IN),
                status=1
            )
            db.add(new_course_assign)
            db.commit()
    return {"status":1, "msg":"User details updated successfully."}




@router.post("/list_user")
async def list_user(
                   db:Session=Depends(deps.get_db),
                   token:str=Form(...),
                   userType:int=Form(...,description="1-> admin 2>Trainer, 3>Student"),
                   user_id: int = Form(None),
                   course_id: int = Form(None),
                   batch_id: int = Form(None),
                   email: str = Form(None),
                   username:str=Form(None),
                   phoneNumber:int=Form(None),
                   page:int=1,
                   size:int=50,
):
    user=deps.get_user_token(db=db,token=token)
    if not user:
        return({'status' :-1,'msg' :'Sorry! your login session expired. please login again.'})
    
    if userType not in[1,2,3]:
        return {"status":0, "msg":"Invalid user type"}
    
    if batch_id:
        get_batch = db.query(Batch).filter(Batch.id==batch_id,Batch.status==1).first()
        if not get_batch:
            return {"status":0, "msg":"Invalid batch"}
    
    get_user = db.query(User).filter(User.status!=-1,User.user_type == userType)

    if batch_id:
        get_user = get_user.filter(User.batch_id==batch_id)
    if course_id:
        get_user = get_user.join(
            CourseAssign, CourseAssign.user_id == User.id).filter(CourseAssign.course_id == course_id)
    if user_id:
        get_user = get_user.filter(User.id == user_id)
    if email:
        get_user = get_user.filter(User.email == email)
    if username:
        get_user = get_user.filter(User.username.ilike(f"%{username}%"))
    if phoneNumber:
        get_user = get_user.filter(User.phone == phoneNumber)

    get_user = get_user.order_by(User.id.desc())
    totalCount= get_user.count()
    total_page,offset,limit=get_pagination(totalCount,page,size)
    get_user=get_user.limit(limit).offset(offset).all()
    dataList =[]    
    
    for data in get_user:
        course_data = []
        get_course = db.query(Course).join(CourseAssign,Course.id==CourseAssign.course_id).filter(CourseAssign.user_id==data.id,CourseAssign.status==1).all()
        if get_course:
            for course in get_course:
                course_data.append({
                    "Course_Id":course.id,
                    "Course_name":course.name
                })
        dataList.append({
            "batch_id":batch_id,
            "id":data.id,
            "name":data.name.capitalize(),
            "username":data.username,
            "email":data.email,
            "user_type":data.user_type,
            "address":data.address,
            # "course_name":  data.course.name if data.course else None,
            # "course_id": data.course_id,
            "phone": data.phone,
            "course":course_data,
            "status":data.status
        })
    data=({"page":page,"size":size,"total_page":total_page,
                "total_count":totalCount,
                "items":dataList})
    return {"status":1,"msg":"Success","data":data}
   
@router.post("/delete_user")
async def deleteUser(db:Session=Depends(get_db),
                     token:str=Form(...),
                     userId:int=Form(...)
):
    
    user  = get_user_token(db,token=token)

    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    if user.user_type == 1 or user.user_type == 2:
        getUser = db.query(User).filter(User.id == userId,User.status == 1).first()

        if not getUser :
            return {"status":0, "msg":"Given user id details not found"}
        
        getUser.status = -1
        db.commit()
        return {"status":1, "msg":"User details successfully deleted"}
    else:
        return {"status":0,"msg":"You are not authenticate to delete the user"}
                
@router.post("/profile")
async def profile(
                    db: Session = Depends(get_db),
                    token: str = Form(...),
):
    user  = get_user_token(db,token=token)

    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    get_course_details = db.query(Course).join(CourseAssign,CourseAssign.course_id==Course.id
                        ).filter(CourseAssign.status==1,CourseAssign.user_id==user.id,Course.status==1).all()
    course_data = []
    for course in get_course_details:
        course_data.append({
            "CourseId":course.id,
            "CourseName":course.name
        })
    return {
        "status":1,
        "msg":"Success",
        "data":{
        "user_id": user.id,
        "name": user.name,
        "username": user.username,
        "phone": user.phone,
        "address": user.address,
        "course": course_data,
        "batch": user.batch.name if user.batch_id else None,
        "user_type": user.user_type,
        "email": user.email,
        "batch_start_date": user.batch.start_date.strftime("%Y-%m-%d") if user.batch_id else None,}
    }
    
@router.post("/active_inactive_user")
async def activeInactiveUser(*,db : Session = Depends(get_db),token:str=Form(...),
                              user_id : int = Form(...),status : int = Form(...,description="1-> active 2-> inactive")):
    user  = get_user_token(db,token=token)
    if status not in [1,2]:
        return {"status":0,"msg":"Invalid status"}
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    if user.user_type != 1:
        return {"status":0,"msg":"Access denied"}
    get_user = db.query(User).filter(User.status != -1,User.id ==user_id).first()
    if not get_user:
        return {"status":0,"msg":"User not found."}
    get_user.status = status
    db.commit()
    msg = "User Inactivated successfully." if status ==2 else "User activated successfully"
    return {"status":1,"msg":msg}