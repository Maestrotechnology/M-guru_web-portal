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
                     user_type:int=Form(...,description=("2>Trainer, 3>Student")),
                     email:EmailStr=Form(...),
                     phone:str=Form(...),
                     address:str=Form(None),
                     password:str=Form(...),
                     course_id:int=Form(None),
                     batch_id:int=Form(None)
                     
):

        
    hashPassword = get_password_hash(password)
    
    user = get_user_token(db,token=token)
    
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}

    if user_type in [2,3]:
        if not course_id:
            return {"status":0,"msg":"Course required"}
    if user_type == 3 and batch_id is None:
        return {"status":0,"msg":"Batch required for student"}
    
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
                    course_id=course_id
                    )
    db.add(addUser)
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
                     course_id:int=Form(None),
                     ):
    
    user  = get_user_token(db,token=token)

    if not user:
        return {"status":0,"msg":"Account details not found"}
    
    checkUser = db.query(User).filter(User.status==1)

    getUser = checkUser.filter(User.id == userId,User.status==1).first()

    if getUser.user_type == 3 and not course_id:
        return {"status":0, "msg": "course is required"}
        
    if not getUser:
        return {"status":0,"msg":"Given user id  not found"}

    # if username:
    #     if checkUser.filter(User.username == username,User.id!=userId).first():
    #         return {"status":0,"msg":"Given userName is already exist"}
    #     getUser.username = username
    if email:
        if checkUser.filter(User.email == email,User.id!=userId).first():
            return {"status":0,"msg":"Given Email is already exist"}
        getUser.email = email
    if phone:
        if checkUser.filter(User.phone==phone,User.id!=userId).first():
            return {"status":0,"msg":"Given Phone Number is already exist"}
    getUser.phone =  phone
    getUser.name=name
    getUser.address=address
    getUser.update_at=datetime.now()
    getUser.course_id=course_id
    db.commit()
    return {"status":1, "msg":"User details updated successfully"}




@router.post("/list_user")
async def list_user(
                   db:Session=Depends(deps.get_db),
                   token:str=Form(...),
                   userType:int=Form(...,description="2>Trainer, 3>Student"),
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
    
    get_user = db.query(User).filter(User.status==1,User.user_type == userType)

    if batch_id:
        get_user = get_user.filter(User.batch_id==batch_id)
    if course_id:
        get_user = get_user.filter(User.course_id==course_id)
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

        dataList.append({
            "batch_id":batch_id,
            "id":data.id,
            "name":data.name.capitalize(),
            "username":data.username,
            "email":data.email,
            "user_type":data.user_type,
            "address":data.address,
            "course_name":  data.course.name if data.course else None,
            "course_id": data.course_id,
            "phone": data.phone
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
    
    return {
        "status":1,
        "msg":"Success",
        "data":{
        "user_id": user.id,
        "name": user.name,
        "username": user.username,
        "phone": user.phone,
        "address": user.address,
        "course": user.course.name if user.course_id else None,
        "batch": user.batch.name if user.batch_id else None,
        "user_type": user.user_type,
        "email": user.email,
        "batch_start_date": user.batch.start_date.strftime("%Y-%m-%d") if user.batch_id else None,}
    }
    

    








    
    