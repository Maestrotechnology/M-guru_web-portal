from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from sqlalchemy import Date,cast

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
@router.post("/checK_in")
async def checK_in(
    *,
    db: Session = Depends(deps.get_db),
    token: str = Form(...),
    check_in_out:int = Form(None,description="1 check in 2 check out"),
    latitude:str=Form(None),
    longitude:str=Form(None),
    Attendance_id:str=Form(None)

):
    user = deps.get_user_token(db=db, token=token)
    if user:
        if not latitude:
            return {"status": 0, "msg": "Latitude is missing"}

        if not longitude:
            return {"status": 0, "msg": "Longitude is missing"}
        if check_in_out==1:
            checkTodayCheckIN = (
            db.query(Attendance)
            .filter(
                Attendance.user_id == user.id,
                cast(Attendance.check_in, Date) == datetime.now(settings.tz_IN).date(),
            )
            .first()
        )
            if checkTodayCheckIN:
                return {"status":-1,"msg":"already you cheked in today"}


            addAttendance = Attendance(
                check_in=datetime.now(settings.tz_IN),
                in_latitude=latitude,
                in_longitude=longitude,
                created_at=datetime.now(settings.tz_IN),
                status=1,
                user_id=user.id
            )
            db.add(addAttendance)
            db.commit()
            addWorkHistory = WorkHistory(
                attendance_id=addAttendance.id,
                break_time=datetime.now(settings.tz_IN),
                status=1,
                created_at=datetime.now(settings.tz_IN),
                
            )
            db.add(addWorkHistory)
            

            db.commit()
        
        if check_in_out==2:
            
            get_Attendance=db.query(Attendance).filter(Attendance.id==Attendance_id,Attendance.status==1).first()
            get_Attendance.out_latitude=latitude
            get_Attendance.out_longitude=longitude
            get_Attendance.check_out=datetime.now(settings.tz_IN)
            db.commit()
        return {"status":1,"msg":"Success"}
    
    else:
        return {'status':-1,"msg":"Your login session expires.Please login later."}


@router.post("/add_task")
async def add_task(
    *,
    db: Session = Depends(deps.get_db),
    token: str = Form(...),
    task_id:int=Form(...), 
    task_detail:int=Form(...),
    Attendance_id:int=Form(...) ,
    expected_time:time=Form(...),
    priority:int=Form(...,description="1-> High 2 -> medium 3 -> low"),
    description:str=Form(None)
):
    user = deps.get_user_token(db=db, token=token)
    if user:
        get_Attendance=db.query(Attendance).filter(Attendance.id==Attendance_id,Attendance.status==1,Attendance.check_out==None).first()
        if not get_Attendance:
            return {
        "status" : -1,
        "msg":"you want to check in"
    }
        addTaskDetail = TaskDetail(
                attendance_id=Attendance_id,
                task_id=task_id,
                description=description,
                status=1,
                created_at=datetime.now(settings.tz_IN),
                user_id=user.id,
                expected_time=expected_time,
                priority=priority
            )
        db.add(addTaskDetail)
        db.commit()
        return {"status":1,"msg":"Success"}
    
    else:
        return {'status':-1,"msg":"Your login session expires.Please login later."}
    

@router.post("/list_task_detail")
async def list_task_detail(
                    db: Session = Depends(get_db),
                    token: str = Form(...),
                    page: int = 1,
                    size: int = 10
):
    user = get_user_token(db,token=token)
    if user:
        priority=["","High","medium","low"]
        get_taskDetail=db.query(TaskDetail).filter(TaskDetail.user_id==user.id,
                                                   TaskDetail.user_id==user.id,
                                                   TaskDetail.status==1,
                                                   ).order_by(TaskDetail.id.desc())
        totalCount= get_taskDetail.count()
        total_page,offset,limit=get_pagination(totalCount,page,size)
        get_taskDetail=get_taskDetail.limit(limit).offset(offset).all()

        data_list = []
        for data in get_taskDetail:
            data_list.append({
                "TaskDetail_id":data.id,
                "attendance_id":data.attendance_id,
                "user_id":data.user_id,
                "user_name":data.user.username,
                "task_id":data.task_id,
                "task_name":data.task.name,
                "expected_time":data.expected_time,
                "priority_id":data.priority,
                "priority_name":priority[data.priority]
            })
        data=({"page":page,"size":size,"total_page":total_page,
                    "total_count":totalCount,
                    "items":data_list})
        return {"status":1,"msg":"Success","data":data}



@router.post("/start_task")
async def start_task(
    *,
    db: Session = Depends(deps.get_db),
    token: str = Form(...),
    action: int = Form(None, description="1>task_started,2>task_paused"),
    close:int = Form(None),
    Attendance_id: int = Form(...),
    task_id:int=Form(...)
    
):
    user = deps.get_user_token(db=db, token=token)

    if user:
        get_Attendance=db.query(Attendance).filter(Attendance.id==Attendance_id,Attendance.status==1,Attendance.check_out==None).first()
        if not get_Attendance:
            return {
        "status" : -1,
        "msg":"you want to check in"
    }

       
        total_work_time = 0
        total_break_time = 0
        task_work_time=0
        get_WorkHistory=db.query(WorkHistory).filter(WorkHistory.status==1)
        get_data=get_WorkHistory.filter(WorkHistory.attendance_id).order_by(WorkHistory.id.desc()).first()
        if action == 1:
            if get_data.work_time!=None:
                return{
        "status" : -1,
        "msg":"already started the work"
    }

            

            last_break_history =get_WorkHistory.filter(
                WorkHistory.attendance_id == Attendance_id,
                WorkHistory.break_time!=None,
                WorkHistory.breakEnd_time == None
            ).first()

            if last_break_history:
                last_break_history.breakEnd_time = datetime.now(settings.tz_IN)
                db.commit()
           
            addWorkHistory = WorkHistory(
                attendance_id=Attendance_id,
                work_time=datetime.now(settings.tz_IN),
                status=1,
                created_at=datetime.now(settings.tz_IN),
                task_id=task_id
            )
            db.add(addWorkHistory)
            db.commit()

        if action == 2:
            if get_data.break_time!=None:
                return{
        "status" : -1,
        "msg":"already started the work"
    }
           
            last_work_history = get_WorkHistory.filter(
                WorkHistory.attendance_id == Attendance_id,
                WorkHistory.work_time!=None,
                WorkHistory.workEnd_time == None  # Only the ongoing work session
            ).first()

            if last_work_history:
                last_work_history.workEnd_time = datetime.now(settings.tz_IN)
                db.commit()

           
            addWorkHistory = WorkHistory(
                attendance_id=Attendance_id,
                break_time=datetime.now(settings.tz_IN),
                status=1,
                created_at=datetime.now(settings.tz_IN),
                task_id=task_id
            )
            db.add(addWorkHistory)
            db.commit()

        if close:
            last_work_history = get_WorkHistory.filter(
                WorkHistory.attendance_id == Attendance_id,
                WorkHistory.workEnd_time == None  # Only the ongoing work session
            ).first()

            if last_work_history:
                last_work_history.workEnd_time = datetime.now(settings.tz_IN)
                db.commit()
            

        
        work_history_records = get_WorkHistory.filter(WorkHistory.attendance_id == Attendance_id).all()

        task_history_records = get_WorkHistory.filter(WorkHistory.attendance_id == Attendance_id,WorkHistory.task_id==task_id).all()
        for record in work_history_records:
            if record.work_time and record.workEnd_time:
               
                work_duration = record.workEnd_time - record.work_time
                total_work_time += work_duration.total_seconds() 

            if record.break_time and record.breakEnd_time:
                
                break_duration = record.breakEnd_time - record.break_time
                total_break_time += break_duration.total_seconds() 
        for record in task_history_records:
            if record.work_time and record.workEnd_time:
               
                work_duration = record.workEnd_time - record.work_time
                task_work_time += work_duration.total_seconds()
        
        return {
            "status" : 1,
            "msg": "Task updated successfully.",
            "total_work_time_hours": total_work_time,
            "total_break_time_hours": total_break_time,
            "task_work_time":task_work_time
        }
        
    
    else:
        return {'status':-1,"msg":"Your login session expires.Please login later."}
    


@router.post("/list_attendance")
async def list_attendance(
                    db: Session = Depends(get_db),
                    token: str = Form(...),
                    check: int = Form(None,description="1->current,2-> overall"),
                    page: int = 1,
                    size: int = 10
):
    user = get_user_token(db,token=token)
    if user:
        check_attendance=db.query(Attendance).filter(Attendance.status==1)
        if check==1:
            get_attendance = (
            check_attendance
            .filter(
                Attendance.user_id == user.id,
                cast(Attendance.check_in, Date) == datetime.now(settings.tz_IN).date(),
            ).first() )
            if get_attendance:
                get_task=db.query(TaskDetail).filter(TaskDetail.status==1,TaskDetail.attendance_id==get_attendance.id).order_by(TaskDetail.id.desc()).first()
                return {'status':1,"msg":"Success","attendance_id":get_attendance.id,"check_in":get_attendance.check_in,"task_id":get_task.task_id if get_task else None }

        if check==2:
            get_attendance=check_attendance.filter(Attendance.user_id==user.id)
        
        totalCount= get_attendance.count()
        total_page,offset,limit=get_pagination(totalCount,page,size)
        get_attendance=get_attendance.limit(limit).offset(offset).all()

        data_list = []
        for data in get_attendance:
            data_list.append({
                "attendance_id":data.id,
                "check_in":data.check_in,
                "check_out":data.check_out
            })
        data=({"page":page,"size":size,"total_page":total_page,
                    "total_count":totalCount,
                    "items":data_list})
        return {"status":1,"msg":"Success","data":data}
    




        



    
    
    

