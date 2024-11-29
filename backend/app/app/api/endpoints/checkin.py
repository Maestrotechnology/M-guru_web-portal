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
@router.post("/add_task")
async def add_task(
    *,
    db: Session = Depends(deps.get_db),
    token: str = Form(...),
    task: str = Form(None),
    description: str = Form(None),
):
    user = deps.get_user_token(db=db, token=token)
    if user:
        if task:
            addWorkReport = WorkReport(
                task=task,
                description=description,
                status=1,
                created_at=datetime.now(settings.tz_IN)
            )
            db.add(addWorkReport)
            db.commit()
        
        
        

@router.post("/start")
async def start(
    *,
    db: Session = Depends(deps.get_db),
    token: str = Form(...),
    task: int = Form(None, description="1>task_started,2>task_paused,3>task_restart"),
    work_report_id: int = Form(...),
):
    user = deps.get_user_token(db=db, token=token)
    if user:
       
        total_work_time = 0
        total_break_time = 0

        if task == 1:
           
            addWorkHistory = WorkHistory(
                work_report_id=work_report_id,
                work_time=datetime.now(settings.tz_IN),
                status=1,
                created_at=datetime.now(settings.tz_IN)
            )
            db.add(addWorkHistory)
            db.commit()

        if task == 2:
           
            last_work_history = db.query(WorkHistory).filter(
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
                created_at=datetime.now(settings.tz_IN)
            )
            db.add(addWorkHistory)
            db.commit()

        if task == 3:
            
            last_break_history = db.query(WorkHistory).filter(
                WorkHistory.work_report_id == work_report_id,
                WorkHistory.break_time != None, 
                WorkHistory.workEnd_time == None 
            ).first()

            if last_break_history:
                last_break_history.workEnd_time = datetime.now(settings.tz_IN)
                db.commit()

            addWorkHistory = WorkHistory(
                work_report_id=work_report_id,
                work_time=datetime.now(settings.tz_IN),
                status=1,
                created_at=datetime.now(settings.tz_IN)
            )
            db.add(addWorkHistory)
            db.commit()

        
        work_history_records = db.query(WorkHistory).filter(WorkHistory.work_report_id == work_report_id).all()

        
        for record in work_history_records:
            if record.work_time and record.workEnd_time:
               
                work_duration = record.workEnd_time - record.work_time
                total_work_time += work_duration.total_seconds() / 3600  # Convert to hours

            if record.break_time and record.workEnd_time:
                
                break_duration = record.workEnd_time - record.break_time
                total_break_time += break_duration.total_seconds() / 3600  # Convert to hours

        
        return {
            "message": "Task updated successfully.",
            "total_work_time_hours": total_work_time,
            "total_break_time_hours": total_break_time
        }