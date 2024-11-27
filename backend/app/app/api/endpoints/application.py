from fastapi import APIRouter,Depends,UploadFile,Form,File
from typing import Annotated
from api.deps import get_db
from sqlalchemy.orm import Session
from pydantic import EmailStr
from app.models import Course,ApplicationDetails,EnquiryType
from core.config import settings
from datetime import datetime
from utils import file_storage

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


