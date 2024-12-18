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
from api.deps import get_db,authenticate,get_by_user,get_user_token,phoneNo_validation,get_username,calculate_distance
from sqlalchemy import func, case

router = APIRouter()
@router.post("/today_checkIn")
async def today_checkIn(
    *,
    db: Session = Depends(deps.get_db),
    token: str = Form(...),
):
    user = deps.get_user_token(db=db, token=token)
    if user:

        today_date = datetime.now(settings.tz_IN).date()

        # Query to get all users, and only filter attendance for today's check-ins
        # Get today's date based on the timezone
        today_date = datetime.now(settings.tz_IN).date()

        # Query to get all users, and only filter attendance for today's check-ins
        checkTodayCheckIN = (
            db.query(User, Attendance)
            .outerjoin(Attendance, Attendance.user_id == User.id)  # Outer join to include all users
            .filter(
                User.status == 1,  # Only active users
                User.batch_id == 13,  # Only users in batch 13
                # Include users with no attendance record at all or attendance record for today
                (cast(Attendance.check_in, Date) == today_date) | (Attendance.id == None)  # Attendance check-in for today OR no attendance record
            )
            .all()
        )
        return checkTodayCheckIN
    


@router.post("/get_student_count")
async def get_student_count(
                db:Session=Depends(get_db),
                # token:str=Form(...)
):
    get_batch = db.query(Batch).filter(Batch.status == 1).first()
    today = datetime.now().date()
    no_of_student_in_batch = len(get_batch.users)
    print(today)
    no_student_present = db.query(Attendance).filter(cast(Attendance.check_in, Date )== today)
    print("no of students absent:",no_of_student_in_batch - no_student_present.count())
    print("no of student present:",no_student_present.count() )
 



@router.post("/application_count")
async def application_count(db: Session = Depends(get_db),token:str=Form(...)):
    user=get_user_token(db=db,token=token)
    if  user.user_type in [1,2]:
    
 
        application = db.query(
            ApplicationDetails.enquiry_id,  EnquiryType.name,
            func.count(ApplicationDetails.enquiry_id).label("total") 
        )\
        .join(EnquiryType, EnquiryType.id == ApplicationDetails.enquiry_id).filter(EnquiryType.status==1,ApplicationDetails.status==1) .group_by(ApplicationDetails.enquiry_id) .all()
        batch_count = db.query(
            User.batch_id,  Batch.name,
            func.count(User.batch_id).label("total") 
        )\
        .join(Batch, Batch.id == User.batch_id).filter(User.status==1,Batch.status==1) .group_by(User.batch_id) .all()

        return {"status":1,"msg":"Success","application_count":application,"batch_count":batch_count}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}
    

   
@router.post("/batch_count")
async def batch_count(db: Session = Depends(get_db)):
 
    get_count = db.query(
        User.batch_id,  Batch.name,
        func.count(User.batch_id).label("total") 
    )\
    .join(Batch, Batch.id == User.batch_id).filter(User.status==1,Batch.status==1) .group_by(User.batch_id) .all()

    return get_count

                       