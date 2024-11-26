from fastapi import APIRouter,Depends,UploadFile,Form
from typing import Annotated
from api.deps import get_db
from sqlalchemy.orm import Session
from pydantic import EmailStr
from app.models import Course,ApplicationDetails,EnquiryType

router = APIRouter()

@router.post("/create_application")
async def createApplication(
                            db: Annotated[Session, Depends(get_db)],
                            name: Annotated[str, Form(...)],
                            email: Annotated[EmailStr, Form(...)],
                            phone: Annotated[str, Form(...)],
                            resume: Annotated[UploadFile, Form(...)],
                            qualification: Annotated[str, Form(...)],
                            passed_out_year: Annotated[str, Form(...)],
                            enquiry_id: Annotated[str, Form(...)],
                            course_id: Annotated[str, Form(...)]
):
    check_enquiry_id = db.query(EnquiryType).filter(EnquiryType.id == enquiry_id).first()
    if not check_enquiry_id:
        return {"status":0, "msg":"Invalid enquiry type"}
    check_course_id = db.query(Course).filter(Course.id == course_id).first()
    if not check_course_id:
        return {"status":0, "msg":"Invalid course"}
    
    application = ApplicationDetails(
        name=name,email=email,phone=phone
    )