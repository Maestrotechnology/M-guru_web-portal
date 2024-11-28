from fastapi import APIRouter,Depends,Form,UploadFile,File
from sqlalchemy.orm import Session
from app.models import *
from app.api.deps import *
from app.core.security import settings
from datetime import datetime
from app.utils import *

router = APIRouter()

@router.post("/create_course_material")
async def createCourseMaterial(
                                db: Session = Depends(get_db),
                                token: str = Form(...),
                                course_id: int = Form(...),
                                description: str = Form(),
                                name: str = Form(),
                                list_material: list[UploadFile] = File(None)
):
    user = get_user_token(token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    course_material = CourseMaterial(
        name = name,
        description = description,
        status = 1,
        created_at = datetime.now(settings.tz_IN),
        updated_at = datetime.now(settings.tz_IN)
    )
    db.add(course_material)
    db.commit()
    if list_material:
        for material in list_material:
            file_path, file_url = file_storage(material, material.filename)
            course_media = CourseMedia()

    
