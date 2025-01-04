from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from sqlalchemy import Date,cast,func

from app.models import ApiTokens,User
from app.api import deps
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime
from app.utils import *
from sqlalchemy import or_
from pydantic import EmailStr
from api.deps import get_db,authenticate,get_by_user,get_user_token,phoneNo_validation,get_username,calculate_distance

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
        if user.user_type!=3:
            return {"status": 0, "msg": "You are not allowed to access"}


        if not latitude:
            return {"status": 0, "msg": "Latitude is missing"}

        if not longitude:
            return {"status": 0, "msg": "Longitude is missing"}
        
        office_lat = 11.091968  
        office_lon =  77.021184 

        
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except:
            return {"status": 0, "msg": "Invalid latitude or longitude format"}

        
        distance = calculate_distance(latitude, longitude, office_lat, office_lon)

        
        # if distance > 200:
        #     return {"status": 0, "msg": "You are too for away from the check in location"}
        if check_in_out==1:
            checkTodayCheckIN = (
            db.query(Attendance)
            .filter(
                Attendance.user_id == user.id,Attendance.status == 1,
                cast(Attendance.check_in, Date) == datetime.now(settings.tz_IN).date(),
            )
            .first()
        )
            if checkTodayCheckIN:
                return {"status":0,"msg":"already you cheked in today"}

                                  
            addAttendance = Attendance(
                check_in=datetime.now(settings.tz_IN),
                in_latitude=latitude,
                in_longitude=longitude,
                created_at=datetime.now(settings.tz_IN),
                status=1,
                user_id=user.id,
                checkIn_status=1


            )
            db.add(addAttendance)
            db.commit()
            return {"status":1,"msg":"check In sucessfully"}
        if check_in_out==2:
            get_task=db.query(TaskDetail).filter(TaskDetail.status==1,TaskDetail.attendance_id==Attendance_id).first()
            if not get_task:
                return {"status":0,"msg":"you want to add the task"}

            get_Attendance=db.query(Attendance).filter(Attendance.id==Attendance_id,Attendance.status==1).first()
            get_Attendance.out_latitude=latitude
            get_Attendance.out_longitude=longitude
            get_Attendance.check_out=datetime.now(settings.tz_IN)
            get_Attendance.checkIn_status=2
            db.commit()
            return {"status":1,"msg":"check out successfully"}
    
    else:
        return {'status':-1,"msg":"Your login session expires.Please login later."}


@router.post("/add_task")
async def add_task(
    *,
    db: Session = Depends(deps.get_db),
    token: str = Form(...),
    task:str=Form(...), 
    Attendance_id:int=Form(...) ,
    expected_time:time=Form(...),
    mentor_time:time=Form(None),
    trainer_id:str=Form(None),
    rating:str=Form(None),
    task_description:str=Form(...),
    mentor_description:str=Form(None),
):
    user = deps.get_user_token(db=db, token=token)
    if user:
        if user.user_type!=3:
            return {"status": 0, "msg": "You are not allowed to access"}
        checkTodayCheckIN = (
            db.query(Attendance)
            .filter(
                Attendance.user_id == user.id,Attendance.id==Attendance_id,
                cast(Attendance.check_in, Date) == datetime.now(settings.tz_IN).date(),
            )
            .first()
        )
        if  not checkTodayCheckIN:
            return {"status":0,"msg":"You want to check In"}
        addTaskDetail = TaskDetail(
                attendance_id=Attendance_id,
                task=task,
                task_description=task_description,
                mentor_description = mentor_description,
                status=1,
                created_at=datetime.now(settings.tz_IN),
                mentor_time=mentor_time,
                student_id=user.id,
                expected_time=expected_time,
                trainer_id=trainer_id,
                rating=rating,
                created_by = user.id
            )
        db.add(addTaskDetail)
        db.commit()
        return {"status":1,"msg":"Task Added Successfully"}
    
    else:
        return {'status':-1,"msg":"Your login session expires.Please login later."}
    

@router.post("/list_task_detail")
async def list_task_detail(
                    db: Session = Depends(get_db),
                    token: str = Form(...),
                    user_id:int=Form(None),
                    from_date : date = Form(None),
                    to_date : date = Form(None),
                    page: int = 1,
                    size: int = 10
):
    user = get_user_token(db,token=token)
    if user:
        today = datetime.now(settings.tz_IN)
        today_date = today.date()
        get_taskDetail=db.query(TaskDetail).filter(TaskDetail.status==1).order_by(TaskDetail.id.desc())
        if user.user_type==3:
            get_taskDetail=get_taskDetail.filter(TaskDetail.student_id==user.id)
        else:
            get_taskDetail=get_taskDetail.filter(TaskDetail.student_id==user_id)
        if from_date or to_date:
            if not from_date:
                from_date = today_date.replace(month=1,day=1)
            if not to_date:
                to_date = today_date
            get_taskDetail = get_taskDetail.filter(func.date(TaskDetail.created_at).between(from_date,to_date))
        totalCount= get_taskDetail.count()
        total_page,offset,limit=get_pagination(totalCount,page,size)
        get_taskDetail=get_taskDetail.limit(limit).offset(offset).all()

        data_list = []
        for data in get_taskDetail:
            data_list.append({
                "TaskDetail_id":data.id,
                "attendance_id":data.attendance_id,
                "user_id":data.student_id,
                "user_name":data.student.username,
                "task":data.task,
                "expected_time":data.expected_time,
                "trainer_id":data.trainer_id,
                "date":data.created_at.strftime("%d-%m-%Y"),
                "trainer_name":data.trainer.username if data.trainer_id!=None else None,
                "task_description":data.task_description,
            })
        data=({"page":page,"size":size,"total_page":total_page,
                    "total_count":totalCount,
                    "items":data_list})
        return {"status":1,"msg":"Success","data":data}
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
            
            
               
            return {'status':1,
                    "msg":"Success",
                    "attendance_id": get_attendance.id if get_attendance else None,
                    "check_in":get_attendance.check_in if get_attendance else None,
                    "checkIn_status":get_attendance.checkIn_status if get_attendance else None
                    }
            
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
    else:
        return {'status':-1,"msg":"Your login session expires.Please login later."}


@router.post("/complete_task")
async def complete_task(
                    db: Session = Depends(get_db),
                    token: str = Form(...),
                    TaskDetail_Id: int = Form(...),
                    
):
    user = get_user_token(db,token=token)
    if user:
        get_TaskDetail=db.query(TaskDetail).filter(TaskDetail.id==TaskDetail_Id).first()
        if get_TaskDetail:
            get_TaskDetail.complete_status=1
            db.commit()
            return {"status":1,"msg":"task completed sucessfully"}
        else:
            return {"status":0,"msg":"Invalid TaskDetail Id"}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login later."}
   
    
@router.post("/list_trainer_rating")
async def list_trainer_rating(
                    db: Session = Depends(get_db),
                    token: str = Form(...),
                    trainer_id:str=Form(...),
                    student_name:str=Form(None),
                    from_date: datetime = Form(None),
                    to_date: datetime = Form(None),
                    page: int = 1,
                    size: int = 10
):
    user = get_user_token(db,token=token)
    if user:
        get_taskDetail=db.query(TaskDetail).filter(
                                                   TaskDetail.trainer_id==trainer_id,
                                                   TaskDetail.status==1).order_by(TaskDetail.id.desc())
        if from_date and to_date:
            get_taskDetail = get_taskDetail.filter(TaskDetail.created_at >= from_date ,TaskDetail.created_at <= to_date)
        if  student_name:
            get_taskDetail = get_taskDetail.join(User,User.id==TaskDetail.student_id).filter(User.status!=1,User.name.like("%"+student_name+"%")).distinct(TaskDetail.id)
        totalCount= get_taskDetail.count()
        total_page,offset,limit=get_pagination(totalCount,page,size)
        get_taskDetail=get_taskDetail.limit(limit).offset(offset).all()

        data_list = []
        for data in get_taskDetail:
            data_list.append({
                "TaskDetail_id":data.id,
                "user_id":data.user_id,
                "name":data.user.name.capitalize(),
                "user_name":data.user.username,
                "task":data.task,
                "description":data.mentor_description,
                "expected_time":data.expected_time,
                "trainer_id":data.trainer_id,
                "trainer_name":data.users.username if data.trainer_id!=None else None,
                "rating":data.rating,
                "created_at":data.created_at
            })
        data=({"page":page,"size":size,"total_page":total_page,
                    "total_count":totalCount,
                    "items":data_list})
        return {"status":1,"msg":"Success","data":data}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login later."}

  
@router.post("/check_out_automatically")
async def check_out_automatically(
                    db: Session = Depends(get_db),
                    token: str = Form(...),
):
    user = get_user_token(db,token=token)
    if user:
        checkTodayCheckIN = db.query(Attendance)\
            .filter(Attendance.status == 1,
                    Attendance.check_out==None,
                    cast(Attendance.check_in, Date) == datetime.now(settings.tz_IN).date())\
                        .update({"check_out":datetime.now(settings.tz_IN)})
        
        db.commit()
        return {"status":1,"msg":"Successfully updated"}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login later."}



@router.post("/trainer_work")
async def trainer_work(
    *,
    db: Session = Depends(deps.get_db),
    token: str = Form(...),
    time_taken:time=Form(...),
    batch_id:int=Form(...),
    taken_date:date=Form(...),
    description:str=Form(None)
):
    user = deps.get_user_token(db=db, token=token)
    if user:
        if user.user_type!=2:
            return {"status": 0, "msg": "You are not allowed to access"}
        addWorkReport = WorkReport(
                trainer_id=user.id,
                date=taken_date,
                description=description,
                status=1,
                taken_time=time_taken,
                created_at=datetime.now(settings.tz_IN),
                batch_id=batch_id,
                created_by = user.id
            )
        db.add(addWorkReport)
        db.commit()
        return {"status":1,"msg":"Successfully created"}

    else:
        return {'status':-1,"msg":"Your login session expires.Please login later."}




@router.post("/list_trainer_work")
async def list_trainer_work(
                    db: Session = Depends(get_db),
                    token: str = Form(...),
                    trainer_id:str=Form(None),
                    from_date: datetime = Form(None),
                    to_date: datetime = Form(None),
                    page: int = 1,
                    size: int = 10
):
    user = get_user_token(db,token=token)
    if user:
        today = datetime.now(settings.tz_IN)
        get_WorkReport=db.query(WorkReport).filter(WorkReport.status==1).order_by(WorkReport.id.desc())
        if user.user_type==1:
            if trainer_id:
                get_WorkReport = get_WorkReport.filter(WorkReport.trainer_id == trainer_id )
        if user.user_type==2:
                get_WorkReport = get_WorkReport.filter(WorkReport.trainer_id == user.id )
        if from_date or to_date:
            if not from_date:
                from_date = today.date().replace(day=1,month=1)
            if not  to_date:
                to_date=today.date()
            get_WorkReport = get_WorkReport.filter(WorkReport.date >= from_date ,WorkReport.date  <= to_date)      
        totalCount= get_WorkReport.count()
        total_page,offset,limit=get_pagination(totalCount,page,size)
        get_WorkReport=get_WorkReport.limit(limit).offset(offset).all()

        data_list = []
        for data in get_WorkReport:
            data_list.append({
                "WorkReport_id":data.id,
                "trainer_id":data.trainer_id,
                "trainer_name":data.trainer.name.capitalize() if data.trainer_id else None ,
                "date":data.date.date(),
                "batch_id":data.batch_id,
                "batch_name":data.batch.name,
                "description":data.description,
                "taken_time":data.taken_time,
                "created_at":data.created_at
            })
        data=({"page":page,"size":size,"total_page":total_page,
                    "total_count":totalCount,
                    "items":data_list})
        return {"status":1,"msg":"Success","data":data}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login later."}
