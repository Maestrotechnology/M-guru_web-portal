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
# @router.post("/today_checkIn")
# async def today_checkIn(
#     *,
#     db: Session = Depends(deps.get_db),
#     token: str = Form(...),
# ):
#     user = deps.get_user_token(db=db, token=token)
#     if user:

#         today_date = datetime.now(settings.tz_IN).date()

#         # Query to get all users, and only filter attendance for today's check-ins
#         # Get today's date based on the timezone
#         today_date = datetime.now(settings.tz_IN).date()

#         # Query to get all users, and only filter attendance for today's check-ins
#         checkTodayCheckIN = (
#             db.query(User, Attendance)
#             .outerjoin(Attendance, Attendance.user_id == User.id)  # Outer join to include all users
#             .filter(
#                 User.status == 1,  # Only active users
#                 User.batch_id == 13,  # Only users in batch 13
#                 # Include users with no attendance record at all or attendance record for today
#                 (cast(Attendance.check_in, Date) == today_date) | (Attendance.id == None)  # Attendance check-in for today OR no attendance record
#             )
#             .all()
#         )
#         return checkTodayCheckIN
    




@router.post("/application_count")
async def application_count(db: Session = Depends(get_db),
                            token:str=Form(...),
                            fromDateTime:datetime=Form(None),
                            toDatetime:datetime=Form(None)):
    user=get_user_token(db=db,token=token)
    if  user.user_type in [1,2]:
        today = datetime.now(settings.tz_IN)
        if toDatetime is None:
            toDatetime = today.replace(hour=23, minute=59, second=59)
        else:
            toDatetime = toDatetime.replace(hour=23, minute=59, second=59)

        if fromDateTime is None:
            fromDateTime = today.replace(day=1, hour=0, minute=0, second=0)
        else:
            fromDateTime = fromDateTime.replace(hour=0, minute=0, second=0)
        
        #application count
        application = db.query(
            ApplicationDetails.enquiry_id.label("enquiry") ,  EnquiryType.name.label("name") ,
            func.count(ApplicationDetails.enquiry_id).label("total") 
        )\
        .join(EnquiryType, EnquiryType.id == ApplicationDetails.enquiry_id)\
            .filter(EnquiryType.status==1,ApplicationDetails.status==1)\
                  .group_by(ApplicationDetails.enquiry_id) 
        
        application_Month=application.filter(ApplicationDetails.created_at.between(fromDateTime,toDatetime)).all()
        aaa=db.query(ApplicationDetails).filter(func.date(ApplicationDetails.created_at)==today.date()).count()
        
        print(aaa,11111)
        application_today=application.filter(func.date(ApplicationDetails.created_at)==today.date()).all()

        application_data_month=[]
        for enquiry,name,count in application_Month:
            application_data_month.append({"enquiry_id":enquiry,
                         "enquiry_name":name,
                         "total":count})
            
        application_data_today=[]
        for enquiry,name,count in application_today:
            application_data_today.append({"enquiry_id":enquiry,
                         "enquiry_name":name,
                         "total":count})
        #batch count 
        batch_count = db.query(
            User.batch_id,  Batch.name,
            func.count(User.batch_id).label("total") 
        )\
        .join(Batch, Batch.id == User.batch_id).filter(User.status==1,Batch.status==1) .group_by(User.batch_id) .all()
        batch_data=[]
        for batch,name,count in batch_count:
            batch_data.append({"batch_id":batch,
                         "batch_name":name,
                         "total":count})
        
        #today present absent
        get_batch = db.query(Batch).filter(Batch.status == 1).first()
        today = datetime.now().date()
        no_of_student_in_batch = len(get_batch.users)
        no_student_present = db.query(Attendance).filter(cast(Attendance.check_in, Date )== today)
        absent=no_of_student_in_batch - no_student_present.count()
        today_attendance={"students_absent":absent,"students_present":no_student_present.count()}
        data=({"application_data_month":application_data_month,"application_data_today":application_data_today,"batch_count":batch_data,"attendance":today_attendance})
        return {"status":1,"msg":"Success","data":data}
        
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}
    

   


                       