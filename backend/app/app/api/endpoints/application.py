from fastapi import APIRouter,Depends,UploadFile,Form,File
from typing import Annotated
from api.deps import get_db
from sqlalchemy.orm import Session
from pydantic import EmailStr
from app.models import Course,ApplicationDetails,EnquiryType,Interview
from core.config import settings
from datetime import datetime
from utils import file_storage,send_mail

router = APIRouter()

@router.post("/captcha_check")
async def captchaCheck(captcha_token: str = Form(...)):
    import requests
 
    response_data = {"secret": settings.SECRET_KEY, "response": captcha_token}
 
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify", data=response_data
    )
 
    if response.status_code == 200:
        response_json = response.json()
        success = response_json.get("success", False)
        error_codes = response_json.get("error-codes", [])
 
        if success:
            return {"status": 1, "msg": "Success"}
        else:
            return {"status": 0, "msg": "Captcha failed", "error_codes": error_codes}
    else:
        return {"status": 0, "msg": "Captcha validation failed with error"}

@router.post("/create_application")
async def createApplication(*,
                            db: Annotated[Session, Depends(get_db)],
                            name: Annotated[str, Form(...)],
                            email: Annotated[EmailStr, Form(...)],
                            phone: Annotated[str, Form(...)],
                            resume: UploadFile = File(None),
                            qualification: Annotated[str, Form(...)],
                            passed_out_year: Annotated[str, Form(...)],
                            enquiry_id: Annotated[int, Form(...)],
                            course_id: Annotated[int, Form(...)]
):
    check_enquiry_id = db.query(EnquiryType).filter(EnquiryType.id == enquiry_id).first()
    if not check_enquiry_id:
        return {"status":0, "msg":"Invalid enquiry type"}
    check_course_id = db.query(Course).filter(Course.id == course_id).first()
    if not check_course_id:
        return {"status":0, "msg":"Invalid course"}
    
    if resume: 
        file_path, file_url = file_storage(resume, resume.filename)
    else:
        file_url = None
    application = ApplicationDetails(           
        name=name,email=email,phone=phone,resume=file_url,qualification=qualification,passed_out_year=passed_out_year,status=1,created_at=datetime.now(settings.tz_IN)
    )
    db.add(application)
    db.commit()
    return {"status":1,"msg":"Successfully submitted"}

@router.post("/update_application")
async def UpdateApplication(*,
                            db: Annotated[Session, Depends(get_db)],
                            application_id: Annotated[int, Form(...)],
                            name: Annotated[str, Form(...)],
                            email: Annotated[EmailStr, Form(...)],
                            phone: Annotated[str, Form(...)],
                            resume: UploadFile = File(None),
                            qualification: Annotated[str, Form(...)],
                            passed_out_year: Annotated[str, Form(...)],
                            enquiry_id: Annotated[int, Form(...)],
                            course_id: Annotated[int, Form(...)]
):
    db_application = db.query(ApplicationDetails).filter(
                                                        ApplicationDetails.id == application_id,
                                                        ApplicationDetails.status == 1
                                                        ).first()
    if not db_application:
        return {"status":0, "msg":"Invalid application"}
    
    check_enquiry_id = db.query(EnquiryType).filter(EnquiryType.id == enquiry_id).first()
    if not check_enquiry_id:
        return {"status":0, "msg":"Invalid enquiry type"}
    check_course_id = db.query(Course).filter(Course.id == course_id).first()
    if not check_course_id:
        return {"status":0, "msg":"Invalid course"}
    if resume: 
        file_path, file_url = file_storage(resume, resume.filename)
    else:
        file_url = None
        
    db_application.name = name
    db_application.email = email
    db_application.phone = phone
    db_application.qualification = qualification
    db_application.passed_out_year = passed_out_year
    db_application.course_id = course_id
    db_application.enquiry_id = enquiry_id
    db_application.resume = file_url

    db.add(db_application)
    db.commit()
    return {"status":1,"msg":"Successfully submitted"}

@router.post("/list_application")
async def listApplication(*,
                            db: Annotated[Session, Depends(get_db)],
                            type: Annotated[int, Form(...,description="1->current_applications , 2->interview , 3->attended , 4-> not selected")],
                            id: Annotated[str, Form(description="multiple ids use (1,2,3) else (1)")] = None,
                            name: Annotated[str, Form()] = None,
                            phone: Annotated[str, Form()] = None,
                            course_id: Annotated[int, Form()] = None,
                            enquiry_id: Annotated[int, Form()] = None,
):
    if type == 1:
        db_applications = db.query(ApplicationDetails).outerjoin(
            Interview,Interview.application_id == ApplicationDetails.id
        ).filter(Interview.id == None,ApplicationDetails.application_status == None,ApplicationDetails.status==1).all()
    elif type == 2:
        db_applications = db.query(ApplicationDetails).join(
            Interview,Interview.application_id == ApplicationDetails.id
        ).filter(Interview.attended_date==None,ApplicationDetails.status==1).all()
    elif type == 3:
        db_applications = db.query(ApplicationDetails).join(
            Interview,Interview.application_id == ApplicationDetails.id
        ).filter(Interview.attended_date!=None,ApplicationDetails.status==1).all()
    elif type == 4:
        db_applications = db.query(ApplicationDetails).filter(
            ApplicationDetails.application_status == 2,ApplicationDetails.status==1
        ).all()
    else:
        return {"status": 0, "msg":"Invaild type"}
    
    if id:
        application_ids = id.split(",")
        db_applications = db_applications.filter(ApplicationDetails.id.in_(application_ids))
    if name:
        db_applications = db_applications.filter(ApplicationDetails.name.ilike(f"%{name}%"))  
    if phone:
        db_applications = db_applications.filter(ApplicationDetails.phone == phone)
    if course_id:
        db_applications = db_applications.filter(ApplicationDetails.course_id == course_id)
    if enquiry_id:
        db_applications = db_applications.filter(ApplicationDetails.enquiry_id == enquiry_id)

    data = []
    for application in db_applications:
        data.append(
            {
                "id":application.id,
                "name":application.name,
                "email":application.email,
                "phone":application.phone,
                "resume":f"{settings.BASEURL}/{application.resume}",
                "qualification":application.qualification,
                "passed_out_year":application.passed_out_year,
                "course_id": application.course_id,
                "course_name": application.courses.name if application.courses else None,  
                "enquiry_id": application.enquiry_id,
                "enquiry_name": application.enquires.name if application.enquires else None,  
            }
        )
    return {
        "status": 1,
        "msg": "Success",
        "data": data,
    }

@router.post("/schedule_interview")
async def scheduleInterview(
                            db: Annotated[Session, Depends(get_db)],
                            application_id: Annotated[int, Form(...)],
                            scheduled_date: datetime = Form(..., description="The scheduled date for the interview")
):
    db_application = db.query(ApplicationDetails).filter(
        ApplicationDetails.id == application_id,
        ApplicationDetails.status == 1
    ).first()

    if not db_application:
        return {"status":0, "msg":"Invalid application"}
    
    await send_mail(db_application.email,f"Success{scheduled_date}")

    create_interview = Interview(
        scheduled_date=scheduled_date,
        application_id=application_id,
        created_at = datetime.now(settings.tz_IN),
        status=1
    )
    db.add(create_interview)
    db.commit()

    return {"status":1, "msg":"Interview scheduled Successfully"}

@router.post("/enter_interview_marks")
async def enterInterviewMarks(
                              db: Annotated[Session, Depends(get_db)],
                              application_id: Annotated[int, Form(...)],
                              attended_date: Annotated[datetime, Form(...)],
                              communication_mark: Annotated[int, Form(...)],
                              aptitude_mark: Annotated[int, Form(...)],
                              programming_mark: Annotated[int, Form(...)],
                              overall_mark: Annotated[int, Form(...)]
):
    db_interview_details = db.query(Interview).filter(
        Interview.application_id == application_id
    ).first()

    if not db_interview_details:
        return {"status":0, "msg":"Invalid application"}
    
    db_interview_details.attended_date = attended_date
    db_interview_details.communication_mark = communication_mark
    db_interview_details.aptitude_mark = aptitude_mark
    db_interview_details.programming_mark = programming_mark
    db_interview_details.overall_mark = overall_mark
    db_interview_details.updated_at = datetime.now(settings.tz_IN)
    db.add(db_interview_details)
    db.commit()

    return {"status":1,"msg":"Mark Updated"}
    





