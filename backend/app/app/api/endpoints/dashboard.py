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
    


@router.post("/aa")
async def aa(
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
 
