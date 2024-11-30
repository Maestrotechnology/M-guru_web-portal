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
@router.post("/checK_in")
async def checK_in(
    *,
    db: Session = Depends(deps.get_db),
    token: str = Form(...),
    check_in_out:int = Form(None,description="1 check in 2 check out"),
    latitude:str=Form(None),
    longitude:str=Form(None),
    WorkReport_id:str=Form(None)

):
    user = deps.get_user_token(db=db, token=token)
    if user:
        if not latitude:
            return {"status": 0, "msg": "Latitude is missing"}

        if not longitude:
            return {"status": 0, "msg": "Longitude is missing"}
        if check_in_out==1:
            addWorkReport = WorkReport(
                check_in=datetime.now(settings.tz_IN),
                in_latitude=latitude,
                in_longitude=longitude,
                created_at=datetime.now(settings.tz_IN)
            )
            db.add(addWorkReport)
            addWorkHistory = WorkHistory(
                work_report_id=WorkReport_id,
                break_time=datetime.now(settings.tz_IN),
                status=1,
                created_at=datetime.now(settings.tz_IN),
            )
            db.add(addWorkHistory)
            

            db.commit()
        
        if check_in_out==2:
            
            get_entry=db.query(WorkReport).filter(WorkReport.id==WorkReport_id,WorkReport.status==1).first()
            get_entry.out_latitude=latitude
            get_entry.out_longitude=longitude
        
            db.commit()
       
        
@router.post("/add_task")
async def add_task(
    *,
    db: Session = Depends(deps.get_db),
    token: str = Form(...),
    task_id:int=Form(...), 
    work_report_id:int=Form(...) ,
    description:int=Form(None)
):
    user = deps.get_user_token(db=db, token=token)
    if user:
        get_WorkReport=db.query(WorkReport).filter(WorkReport.id==work_report_id,WorkReport.status==1,WorkReport.check_out==None).first()
        if not get_WorkReport:
            return {
        "status" : -1,
        "msg":"you want to check in"
    }
        addTaskDetail = TaskDetail(
                work_report_id=work_report_id,
                task_id=task_id,
                description=description,
                status=1,
                created_at=datetime.now(settings.tz_IN)
            )
        db.add(addTaskDetail)
        db.commit()



@router.post("/start_task")
async def start_task(
    *,
    db: Session = Depends(deps.get_db),
    token: str = Form(...),
    action: int = Form(None, description="1>task_started,2>task_paused"),
    close:int = Form(None),
    work_report_id: int = Form(...),
    task_id:int=Form(...)
    
):
    user = deps.get_user_token(db=db, token=token)

    if user:
        get_WorkReport=db.query(WorkReport).filter(WorkReport.id==work_report_id,WorkReport.status==1,WorkReport.check_out==None).first()
        if not get_WorkReport:
            return {
        "status" : -1,
        "msg":"you want to check in"
    }

       
        total_work_time = 0
        total_break_time = 0
        task_work_time=0
        get_WorkHistory=db.query(WorkHistory).filter(WorkHistory.status==1)
        if action == 1:
            last_break_history =get_WorkHistory.filter(
                WorkHistory.work_report_id == work_report_id,
                WorkHistory.breakEnd_time == None
            ).first()

            if last_break_history:
                last_break_history.breakEnd_time = datetime.now(settings.tz_IN)
                db.commit()
           
            addWorkHistory = WorkHistory(
                work_report_id=work_report_id,
                work_time=datetime.now(settings.tz_IN),
                status=1,
                created_at=datetime.now(settings.tz_IN),
                task_id=task_id
            )
            db.add(addWorkHistory)
            db.commit()

        if action == 2:
           
            last_work_history = get_WorkHistory.filter(
                WorkHistory.work_report_id == work_report_id,
                WorkHistory.workEnd_time == None  # Only the ongoing work session
            ).first()

            if last_work_history:
                last_work_history.workEnd_time = datetime.now(settings.tz_IN)
                db.commit()

           
            addWorkHistory = WorkHistory(
                work_report_id=work_report_id,
                break_time=datetime.now(settings.tz_IN),
                status=1,
                created_at=datetime.now(settings.tz_IN),
                task_id=task_id
            )
            db.add(addWorkHistory)
            db.commit()

        if close:
            last_work_history = get_WorkHistory.filter(
                WorkHistory.work_report_id == work_report_id,
                WorkHistory.workEnd_time == None  # Only the ongoing work session
            ).first()

            if last_work_history:
                last_work_history.workEnd_time = datetime.now(settings.tz_IN)
                db.commit()

        
        work_history_records = get_WorkHistory.filter(WorkHistory.work_report_id == work_report_id).all()

        task_history_records = get_WorkHistory.filter(WorkHistory.work_report_id == work_report_id,WorkHistory.task_id==task_id).all()
        for record in work_history_records:
            if record.work_time and record.workEnd_time:
               
                work_duration = record.workEnd_time - record.work_time
                total_work_time += work_duration.total_seconds() 

            if record.break_time and record.workEnd_time:
                
                break_duration = record.workEnd_time - record.break_time
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