from fastapi import APIRouter, Depends, Form, UploadFile,File
from sqlalchemy.orm import Session
from app.models import *
from app.core.config import settings
from datetime import datetime
from app.utils import *
from api.deps import get_db,get_user_token

router = APIRouter()

@router.post("/upload_project")
async def uploadProject(
                            db: Session = Depends(get_db),
                            token: str = Form(...),
                            project_start_date: datetime = Form(...),
                            project_end_date: datetime = Form(...),
                            description: str = Form(None),
                            project_url: UploadFile = File(...),
                            task_id: int = Form(...)
):
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    file_path, file_url = file_storage(project_url, project_url.filename)
    create_project = StudentProjectDetail(
        project_start_date = project_start_date,
        project_end_date = project_end_date,
        description = description,
        task_id = task_id,
        user_id = user.id,
        project_url = file_url,
        created_at = datetime.now(settings.tz_IN),
        updated_at = datetime.now(settings.tz_IN),
        status = 1
    )
    db.add(create_project)
    db.commit()
    return {"status":1, "msg":"Successfully project submitted"}


@router.post("/list_student_project")
async def listStudentProject(
                                db: Session = Depends(get_db),
                                token: str = Form(...),
                                batch_id: int = Form(None),
                                course_id: int = Form(None),
                                task_id: int = Form(None),
):
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    get_students = db.query(User).filter(User.status==1)
    if user.user_type in [1,2]:
        if not batch_id:
            return {"status":0,"msg":"batch is required"}
        get_students = get_students.filter(User.batch_id == batch_id)
        if course_id:
            get_students = get_students.filter(User.course_id == course_id)
        if task_id:
            get_students = get_students.join(
                StudentProjectDetail,
                StudentProjectDetail.user_id == User.id
            ).filter(
                StudentProjectDetail.task_id == task_id
            )
        
        

        
