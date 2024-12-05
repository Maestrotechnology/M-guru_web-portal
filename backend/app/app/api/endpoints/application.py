from fastapi import APIRouter,Depends,UploadFile,Form,File
from typing import Annotated
from api.deps import *
from sqlalchemy.orm import Session
from pydantic import EmailStr
from app.models import *
from core.config import settings
from datetime import datetime
from utils import file_storage,send_mail,get_pagination
from app.api.endpoints.email_templetes import get_email_templete

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
                            token: str = Form(...),
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
    user = get_user_token(db=db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}  
    if user.user_type != 1:
        return {"status":0,"msg":"Access denied"}
    get_applications = db.query(ApplicationDetails).filter(ApplicationDetails.status==1,ApplicationDetails.email==email).first()
    if get_applications:
        return {"status":0,"msg":"Give Email is already exist"}
    get_user = db.query(ApplicationDetails).filter(ApplicationDetails.status==1,ApplicationDetails.phone==phone).first()
    if get_user:
        return {"status":0,"msg":"Given Phone Number is already exist"}
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
        name=name,email=email,phone=phone,resume=file_url,qualification=qualification,passed_out_year=passed_out_year,status=1,created_at=datetime.now(settings.tz_IN),course_id=course_id,enquiry_id=enquiry_id
    )
    db.add(application)
    db.commit()
    return {"status":1,"msg":"Successfully submitted"}

@router.post("/update_application")
async def updateApplication(*,
                            token: str = Form(...),
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
    user = get_user_token(db=db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}  
    if user.user_type != 1:
        return {"status":0,"msg":"Access denied"}
    
    db_application = db.query(ApplicationDetails).filter(
                                                        ApplicationDetails.id == application_id,
                                                        ApplicationDetails.status == 1
                                                        ).first()
    if not db_application:
        return {"status":0, "msg":"Invalid application"}
    
    get_applications = db.query(ApplicationDetails).filter(ApplicationDetails.id!=application_id,ApplicationDetails.status==1,ApplicationDetails.email==email).first()
    if get_applications:
        return {"status":0,"msg":"Give Email is already exist"}
    get_user = db.query(ApplicationDetails).filter(ApplicationDetails.id!=application_id,ApplicationDetails.status==1,ApplicationDetails.phone==phone).first()
    if get_user:
        return {"status":0,"msg":"Given Phone Number is already exist"}
    
    check_enquiry_id = db.query(EnquiryType).filter(EnquiryType.id == enquiry_id).first()
    if not check_enquiry_id:
        return {"status":0, "msg":"Invalid enquiry type"}
    check_course_id = db.query(Course).filter(Course.id == course_id).first()
    if not check_course_id:
        return {"status":0, "msg":"Invalid course"}
    if resume: 
        file_path, file_url = file_storage(resume, resume.filename)
        db_application.resume = file_url

        
    db_application.name = name
    db_application.email = email
    db_application.phone = phone
    db_application.qualification = qualification
    db_application.passed_out_year = passed_out_year
    db_application.course_id = course_id
    db_application.enquiry_id = enquiry_id

    db.add(db_application)
    db.commit()
    return {"status":1,"msg":"Successfully submitted"}

@router.post("/list_application")
async def listApplication(*,
                            token: str = Form(...),
                            db: Annotated[Session, Depends(get_db)],
                            type: Annotated[int, Form(...,description="1->current_applications , 2->interview , 3->attended , 4-> not selected, 5-> selected, 6->waiting list")],
                            id: Annotated[str, Form(description="multiple ids use (1,2,3) else (1)")] = None,
                            name: Annotated[str, Form()] = None,
                            phone: Annotated[str, Form()] = None,
                            course_id: Annotated[int, Form()] = None,
                            enquiry_id: Annotated[int, Form()] = None,
                            page: Annotated[int, Form()] = 1,
                            size: Annotated[int, Form()] = 10,
):
    user = get_user_token(db=db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}  
    if user.user_type != 1:
        return {"status":0,"msg":"Access denied"}
    if type == 1:#current_applications
        db_applications = db.query(ApplicationDetails).outerjoin(
            Interview,Interview.application_id == ApplicationDetails.id
        ).filter(Interview.id == None,ApplicationDetails.application_status == None,ApplicationDetails.status==1)
    elif type == 2:#interview
        db_applications = db.query(ApplicationDetails).join(
            Interview,Interview.application_id == ApplicationDetails.id
        ).filter(Interview.attended_date==None,ApplicationDetails.status==1)
    elif type == 3:#attended
        db_applications = db.query(ApplicationDetails).join(
            Interview,Interview.application_id == ApplicationDetails.id
        ).filter(Interview.attended_date!=None,ApplicationDetails.status==1)
    elif type == 4:#not selected
        db_applications = db.query(ApplicationDetails).filter(
            ApplicationDetails.application_status == 2,ApplicationDetails.status==1
        )
    elif type == 5:#selected
        db_applications = db.query(ApplicationDetails).filter(
            ApplicationDetails.application_status == 1,ApplicationDetails.status==1
        )
    elif type == 6:#waiting list
        db_applications = db.query(ApplicationDetails).filter(
            ApplicationDetails.application_status == 3,ApplicationDetails.status==1
        )
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

    application_count = db_applications.count()
    totalPages,offset,limit = get_pagination(application_count,page,size)
    db_applications = db_applications.order_by(ApplicationDetails.id.desc()).limit(limit).offset(offset).all()

    data_list = []
    for application in db_applications:
        data_list.append(
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
                "scholarship": application.scholarship,
                "interview_scheduled_date": application.interview_details.scheduled_date if application.interview_details else None,
                "interview_attended_date": application.interview_details.attended_date if application.interview_details else None,
                "communication_mark": application.interview_details.communication_mark if application.interview_details else None,
                "aptitude_mark": application.interview_details.aptitude_mark if application.interview_details else None,
                "programming_mark": application.interview_details.programming_mark if application.interview_details else None,
                "overall_mark": application.interview_details.overall_mark if application.interview_details else None,
                "application_status": application.application_status,
                "batch_id": application.batch_id
            }
        )
    data=({"page":page,
           "size":size,
           "total_page":totalPages,
           "total_count":application_count,
           "items":data_list})
            
    return ({"status":1,"msg":"Success.","data":data})

@router.post("/delete_application")
async def deleteApplication(*,
                            token: str = Form(...),
                            db: Annotated[Session, Depends(get_db)],
                            application_id: Annotated[int, Form(...)]
):
    user = get_user_token(db=db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}  
    if user.user_type != 1:
        return {"status":0,"msg":"Access denied"}
    db_application = db.query(ApplicationDetails).filter(ApplicationDetails.id == application_id, ApplicationDetails.status==1).first()
    if not db_application:
        return {"status":0,"msg":"Application not found"}
    db_application.status=-1
    db.add(db_application)
    db.commit()
    return {"status":1,"msg":"Application successfully deleted"}


@router.post("/schedule_interview")
async def scheduleInterview(*,
                            token: str = Form(...),
                            db: Annotated[Session, Depends(get_db)],
                            application_id: Annotated[int, Form(...)],
                            scheduled_date: datetime = Form(None,description="The scheduled date for the interview"),
                            application_status: Annotated[int, Form(description="1-> seleted 2->not seleted ")]=None
):
    user = get_user_token(db=db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}  
    if user.user_type != 1:
        return {"status":0,"msg":"Access denied"}
    db_application = db.query(ApplicationDetails).filter(
        ApplicationDetails.id == application_id,
        ApplicationDetails.status == 1
    ).first()

    if not db_application:
        return {"status":0, "msg":"Invalid application"}
    
    if application_status==1:
        if not scheduled_date:
            return {"status":0, "msg":"Please enter interview date"}
        
        await send_mail(receiver_email=db_application.email,message=get_email_templete(db_application,scheduled_date,application_status),subject="Application status")

        create_interview = Interview(
            scheduled_date=scheduled_date,
            application_id=application_id,
            created_at = datetime.now(settings.tz_IN),
            status=1
        )
        db.add(create_interview)
        db.commit()

        return {"status":1, "msg":"Interview scheduled Successfully"}
    elif application_status==2:

        await send_mail(receiver_email=db_application.email,message=get_email_templete(db_application,scheduled_date,application_status),subject="Application status")
        db_application.application_status=2
        db.add(db_application)
        db.commit()
        return {"status":1, "msg":"Mail sent Successfully"}
    elif application_status==3:
        db_application.application_status=3
        db.add(db_application)
        db.commit()
        return {"status":1, "msg":"Application successfully moved to waiting list"}

@router.post("/enter_interview_marks")
async def enterInterviewMarks(*,
                              token: str = Form(...),
                              db: Annotated[Session, Depends(get_db)],
                              application_id: Annotated[int, Form(...)],
                              attended_date: Annotated[datetime, Form(...)],
                              communication_mark: Annotated[int, Form(...)],
                              aptitude_mark: Annotated[int, Form(...)],
                              programming_mark: Annotated[int, Form(...)],
                              overall_mark: Annotated[int, Form(...)],
                              application_status: Annotated[int, Form(description="1-> seleted 2->not seleted 3->waiting list")]=None,
                              scholarship: Annotated[int, Form()] = None
):
    user = get_user_token(db=db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}  
    if user.user_type != 1:
        return {"status":0,"msg":"Access denied"}
    db_interview_details = db.query(Interview).filter(
        Interview.application_id == application_id
    ).first()

    if not db_interview_details:
        return {"status":0, "msg":"Invalid interview details"}
    if application_status==1:
        db_interview_details.application.application_status=1
        db_interview_details.application.scholarship=scholarship
    elif application_status==2:
        db_interview_details.application.application_status=2
    elif application_status==3:
        db_interview_details.application.application_status=3

    db_interview_details.attended_date = attended_date
    db_interview_details.communication_mark = communication_mark
    db_interview_details.aptitude_mark = aptitude_mark
    db_interview_details.programming_mark = programming_mark
    db_interview_details.overall_mark = overall_mark
    db_interview_details.updated_at = datetime.now(settings.tz_IN)
    db.add(db_interview_details)
    db.commit()

    return {"status":1,"msg":"Mark Updated"}
    





