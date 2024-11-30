from fastapi import APIRouter,Depends,UploadFile,Form,File
from typing import Annotated
from api.deps import *
from sqlalchemy.orm import Session
from pydantic import EmailStr
from app.models import *
from core.config import settings
from datetime import datetime
from utils import file_storage,send_mail,get_pagination


router = APIRouter()

@router.post("/create_task")
async def createTask(
                      db: Session = Depends(get_db),
                      token: str = Form(...),
                      name: str = Form(...)
):
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    task = Task(
        name=name,
        status=1,
        created_at=datetime.now(settings.tz_IN),
        updated_at=datetime.now(settings.tz_IN),
        created_by_user_id=user.id
        )
    db.add(task)
    db.commit()
    return {"status":1,"msg":"Task created successfully"}

@router.post("/list_task")
async def listTask(
                    db: Session = Depends(get_db),
                    token: str = Form(...),
                    name: str = Form(None),
                    task_id: int = Form(None),
                    page: int = 1,
                    size: int = 10
):
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    

    get_task = db.query(Task).filter(Task.status == 1)

    if task_id:
        get_task = get_task.filter(Task.id == task_id)
    if name:
        get_task = get_task.filter(Task.name.like(f"%{name}%"))

    get_task = get_task.order_by(Task.name)
    totalCount= get_task.count()
    total_page,offset,limit=get_pagination(totalCount,page,size)
    get_task=get_task.limit(limit).offset(offset).all()

    data_list = []
    for data in get_task:
        data_list.append({
            "id":data.id,
            "created_by":data.created_by.name,
            "name":data.name
        })
    data=({"page":page,"size":size,"total_page":total_page,
                "total_count":totalCount,
                "items":data_list})
    return {"status":1,"msg":"Success","data":data}

@router.post("/update_task")
async def updateTask(
                      db: Session = Depends(get_db),
                      token: str = Form(...),
                      task_id: int = Form(...),
                      name: str = Form(...) 
):
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    get_task = db.query(Task).filter(Task.status==1,Task.id == task_id).first()
    if not get_task:
        return {"status":0,"msg":"Task not found"}
    get_task.name = name
    db.add(get_task)
    db.commit()
    return {"status":1,"msg":"Task updated successfully"}

@router.post("/delete_task")
async def deleteTask(
                      db: Session = Depends(get_db),
                      token: str = Form(...),
                      task_id: int = Form(...),
):
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    get_task = db.query(Task).filter(Task.status==1,Task.id == task_id).first()
    if not get_task:
        return {"status":0,"msg":"Task not found"}
    get_task.status = -1
    db.add(get_task)
    db.commit()
    return {"status":1,"msg":"Task deleted successfully"}