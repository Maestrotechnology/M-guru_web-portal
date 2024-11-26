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

@router.post("/create_user")
async def createUser(db:Session=Depends(get_db),
                     token:str = Form(...),
                     name:str = Form(...),
                     user_type:int=Form(...,description=("2>Trainer, 3>Student")),
                     username:str=Form(...),
                     email:EmailStr=Form(...),
                     phone:str=Form(...),
                     address:int=Form(...),

                     password:str=Form(...)):
    
    hashPassword = get_password_hash(password)

    
    user = get_user_token(db,token=token)
    

    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}

    # to check duplicate username
    getUser =  get_by_user(db,username=username)

    if getUser:
        return {"status":0,"msg":"Given Username is already exist"}
    
    checkUser = db.query(User).filter(User.status==1)

    if checkUser.filter(User.email == email).first():
        return {"status":0,"msg":"Give Email is already exist"}
    if checkUser.filter(User.phone==phone).first():
        return {"status":0,"msg":"Given Phone Number is already exist"}
    
    addUser =  User(
                    name=name,
                    username = username,
                    user_type=user_type,
                    email=email,
                    phone=phone,
                    password=hashPassword,
                    created_at = datetime.now(),
                    status =1,
                    address=address
                    )
    db.add(addUser)
    db.commit()
    return {
        "status" : 1,
        "msg":"User created successfully"
    }

@router.post("/update_user")
async def updateUser(db:Session=Depends(get_db),
                     token:str=Form(...),
                     userId:int=Form(...),
                     username:str = Form(None),
                     name:str = Form(None),
                     email:EmailStr = Form(None),
                     phone:str= Form(None),
                     address:str=Form(None)
                     ):
    
    user  = get_user_token(db,token=token)

    if not user:
        return {"status":0,"msg":"Account details not found"}
    
    checkUser = db.query(User).filter(User.status==1)

    getUser = checkUser.filter(User.id == userId,User.status==1).first()

    if not getUser:
        return {"status":0,"msg":"Given user id  not found"}

    if username:
        if checkUser.filter(User.username == username,User.id!=userId).first():
            return {"status":0,"msg":"Given userName is already exist"}
        getUser.username = username
    if email:
        if checkUser.filter(User.email == email,User.id!=userId).first():
            return {"status":0,"msg":"Given Email is already exist"}
        getUser.email = email
    if phone:
        if checkUser.filter(User.phone==phone,User.id!=userId).first():
            return {"status":0,"msg":"Given Phone Number is already exist"}
        getUser.phone =  phone
    if name:
        getUser.name=name

    if address:
        getUser.address=address

    getUser.updated_at=datetime.now()
    

    db.commit()

    return {"status":1, "msg":"User details updated successfully"}




@router.post("/list_user")
async def list_user(db:Session=Depends(deps.get_db),
                   token:str=Form(...),page:int=1,
                   size:int=10,
                   userType:int=Form(...,description="2>Trainer, 3>Student"),
                   username:str=Form(None),
                   phoneNumber:int=Form(None)):
    user=deps.get_user_token(db=db,token=token)
    if user:
        getuser =  db.query(User).\
            filter(User.userType == userType,
                User.status ==1 )
        if username:
            getuser = getuser.filter(User.username.like("%"+username+"%"))
        if phoneNumber:
            getuser = getuser.filter(User.phone.like("%"+str(phoneNumber)+"%"))

        getuser = getuser.order_by(User.id.desc())
        totalCount= getuser.count()
        total_page,offset,limit=get_pagination(totalCount,page,size)
        getuser=getuser.limit(limit).offset(offset).all()
        dataList =[]

        for row in getuser:
            dataList.append({
                "user_id" :row.id,
                "name":row.name,
                "user_name":row.username,
                "email":row.email,
                "phone_number":row.phone,
                "status":row.status,
                "user_type":row.user_type
            })
        data=({"page":page,"size":size,"total_page":total_page,
                "total_count":totalCount,
                "items":dataList})
        return {"status":1,"msg":"Success","data":data}
    

    else:
        return({'status' :-1,
                'msg' :'Sorry! your login session expired. please login again.'}) 
    

@router.post("/delete_user")
async def deleteUser(db:Session=Depends(get_db),
                     token:str=Form(...),
                     userId:int=Form(...)):
    
    user  = get_user_token(db,token=token)

    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    if user.userType == 1 or user.userType == 2:
        getUser = db.query(User).filter(User.id == userId,User.status == 1).first()

        if not getUser :
            return {"status":0, "msg":"Given user id details not found"}
        
        getUser.status = -1
        db.commit()
        return {"status":1, "msg":"User details successfully deleted"}
    else:
        return {"status":0,"msg":"You are not authenticate to delete the user"}
                

@router.post("/view_user")
async def view_user(db:Session=Depends(get_db),
                     token:str=Form(...),
                     userId:int=Form(...)):
    user=deps.get_user_token(db=db,token=token)
    if not user:
        return({'status' :-1,
                'msg' :'Sorry! your login session expired. please login again.'}) 
    getuser =  db.query(User).\
                filter(User.id == userId,
                    User.status ==1 ).all()
    if not getuser :
            return {"status":0, "msg":"Given user id details not found"}

   
    dataList={
                "user_id" :getuser.id,
                "name":getuser.name,
                "user_name":getuser.username,
                "email":getuser.email,
                "phone_number":getuser.phone,
                "status":getuser.status,
                "user_type":getuser.user_type
            }

    return {"status":1,"msg":"Success","data":dataList}







    
    