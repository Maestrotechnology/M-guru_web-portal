from fastapi import APIRouter,Depends,UploadFile,Form,File
from typing import Annotated
from api.deps import *
from sqlalchemy.orm import Session
from sqlalchemy import or_,and_
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
                      name: str = Form(...),
                      task_report_url: UploadFile = File(None),
                      from_date: datetime = Form(None),
                      end_date: datetime = Form(None),
                      description: str = Form(None),
                      course_id: int = Form(...),
):
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    check_task = db.query(Task).filter(Task.name==name,Task.course_id==course_id,Task.status==1).first()
    if check_task:
        return {"status":0,"msg":"Task already exits."}
    if task_report_url:
        file_path, file_url = file_storage(task_report_url, task_report_url.filename)
    else:
        file_url = None
    task = Task(
            name=name,
            status=1,
            task_report_url = file_url,
            from_date = from_date,
            end_date = end_date,
            description = description,
            created_at=datetime.now(settings.tz_IN),
            updated_at=datetime.now(settings.tz_IN),
            created_by=user.id,
            course_id = course_id,
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
                    course_id: int = Form(None),
                    # batch_id: int = Form(None),
                    page:int=1,
                    size:int=50,
):
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    

    get_task = db.query(Task).filter(Task.status == 1)
    if user.user_type ==2:
            course = []
            get_assigned_course = db.query(CourseAssign).filter(CourseAssign.status==1,CourseAssign.user_id==user.id).all()
            for assigned_course in get_assigned_course:
                course.append(assigned_course.course_id)
            get_task = get_task.filter(Task.course_id.in_(course)).distinct(Task.id)

    if user.user_type == 3:   
            course = []
            get_assigned_course = db.query(CourseAssign).filter(CourseAssign.status==1,CourseAssign.user_id==user.id).all()
            for assigned_course in get_assigned_course:
                course.append(assigned_course.course_id)
            get_task = get_task.join(TaskAssign,TaskAssign.batch_id==user.batch_id).filter(
                Task.course_id.in_(course),TaskAssign.status ==1
                # and_(Task.batch_id==user.batch_id,
                # Task.course_id == None)
                ).distinct(Task.id)

    if task_id:
        get_task = get_task.filter(Task.id == task_id)
    if name:
        get_task = get_task.filter(Task.name.like(f"%{name}%"))
    if course_id:
        get_task = get_task.filter(Task.course_id == course_id)
    # if batch_id:
    #     get_task = get_task.filter(Task.batch_id == batch_id)

    get_task = get_task.order_by(Task.name)
    totalCount= get_task.count()
    total_page,offset,limit=get_pagination(totalCount,page,size)
    get_task=get_task.limit(limit).offset(offset).all()

    data_list = []
    for data in get_task:
        batch_list = []
        get_all_batch = db.query(Batch).join(TaskAssign,TaskAssign.batch_id==Batch.id).filter(TaskAssign.status==1,TaskAssign.task_id==data.id, Batch.status==1).all()
        if get_all_batch:
            for batch in get_all_batch:
                batch_list.append({
                    "Batch_Id":batch.id,
                    "Batch_name":batch.name
                })
        data_list.append({
            "id":data.id,
            "created_by":data.user.name.capitalize() if data.created_by else None,
            "name":data.name.capitalize(),
            "task_report_url": f"{settings.BASEURL}/{data.task_report_url}" if data.task_report_url else None,
            "from_date": data.from_date.strftime("%Y-%m-%d %H:%M:%S") if data.from_date else None,
            "end_date": data.end_date.strftime("%Y-%m-%d %H:%M:%S") if data.end_date else None,
            "description": data.description,
            "course_id": data.course_id,
            "course_name": data.course.name if data.course else None,
            "batch": batch_list,
            # "batch_name": data.batch.name if data.batch else None
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
                      name: str = Form(...),
                      task_report_url: UploadFile = File(None),
                      from_date: datetime = Form(None),
                      end_date: datetime = Form(None),
                      description: str = Form(None),
                      course_id: int = Form(...),
                    #   batch_id: str = Form(None,description="if multiple -> 1,2,3,4,5") 
):
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    get_task = db.query(Task).filter(Task.status==1,Task.id == task_id).first()
    if not get_task:
        return {"status":0,"msg":"Task not found"}
    
    if task_report_url:
        file_path, file_url = file_storage(task_report_url, task_report_url.filename)
        get_task.task_report_url = file_url
    get_task.from_date = from_date
    get_task.end_date = end_date
    get_task.description = description
    get_task.course_id = course_id
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

@router.post("/list_task_score")
async def listTaskScore(
                        db: Session = Depends(get_db),
                        token: str = Form(...),
                        task_id: int = Form(...),
                        name: str = Form(None),
                        username: str = Form(None),
                        page: int = 1,
                        size: int = 50
):
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    if user.user_type not in [1,2]:
        return {"status":0,"msg":"Access denied"}
    """
    In below query im getting , active batch users score
    """
    get_score = db.query(Score).join(
        Task,Task.id == Score.task_id,
    ).join(
        User,
        User.id == Score.student_id
    ).join(
        Batch,
        User.batch_id == Batch.id
    ).filter(Batch.status==1,Task.id==task_id,Score.status==1)

    if name:
        get_score = get_score.filter(User.name.ilike(f"%{name}%"))
    if username:
        get_score = get_score.filter(User.username.ilike(f"%{username}%"))

    get_score = get_score.order_by(Score.id.desc())
    totalCount= get_score.count()
    total_page,offset,limit=get_pagination(totalCount,page,size)
    get_score=get_score.limit(limit).offset(offset).all()

    data_list = []
    for data in get_score:
        data_list.append({
            "score_id": data.id,
            "student_name": data.student.name.capitalize(),
            "student_username": data.student.username,
            # "course_name": data.student.course.name if data.student.course else None,
            "student_id": data.student.id,
            "mark": data.mark,
            "description": data.description,
            "mark_giver": data.teacher.name,
            "tast_id": data.task_id,
            "task_name": data.task.name,
            "mark_given_date": data.created_at
        })


    data=({"page":page,"size":size,"total_page":total_page,
                "total_count":totalCount,
                "items":data_list})
    return {"status":1,"msg":"Success","data":data}

@router.post("/assign_task")
async def assignTask(db: Session = Depends(get_db),
                        token: str = Form(...),
                        task_id: int = Form(...),
                        batch_ids:str=Form(...,description="if multiple 1,2,3,4,5,6")
):
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    check_task = db.query(Task).filter(Task.id == task_id,Task.status==1).first()
    if not check_task:
        return {"status":0,"msg":"Task not found."}
    batch_id = [int(batch) for batch in batch_ids.split(",")]
    assigned_batch = db.query(TaskAssign).filter(TaskAssign.task_id==task_id).all()
    
    for batch in assigned_batch:
        if batch.batch_id not in batch_id:
            batch.status=-1
            batch.update_at = datetime.now(settings.tz_IN)
            db.commit()
        else:
            if batch.status !=1:
                batch.status =1
                batch.update_at = datetime.now(settings.tz_IN)
                db.commit()
            batch_id.remove(batch.batch_id)
    
    for batch in batch_id:
        new_batch_assign = TaskAssign(
            task_id = task_id,
            batch_id = batch,
            created_by = user.id,
            created_at = datetime.now(settings.tz_IN),
            status=1
        )
        db.add(new_batch_assign)
        db.commit()
    return {"status":1,"msg":"Assigned Successfully"}