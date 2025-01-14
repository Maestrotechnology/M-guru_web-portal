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
    check_task_detail = db.query(StudentProjectDetail).filter(StudentProjectDetail.task_id==task_id,
                            StudentProjectDetail.student_id==user.id,StudentProjectDetail.status==1).first()
    if check_task_detail:
        return {"status":0,"msg":"You have already submitted the file"}
    create_project = StudentProjectDetail(
        project_start_date = project_start_date,
        project_end_date = project_end_date,
        description = description,
        task_id = task_id,
        student_id = user.id,
        project_url = file_url,
        created_at = datetime.now(settings.tz_IN),
        # updated_at = datetime.now(settings.tz_IN),
        status = 1,
        created_by = user.id,
        is_marked =0,
    )
    db.add(create_project)
    db.commit()
    return {"status":1, "msg":"Successfully project submitted"}


# @router.post("/list_student_project")
# async def listStudentProject(
#                                 db: Session = Depends(get_db),
#                                 token: str = Form(...),
#                                 # batch_id: int = Form(None),
#                                 course_id: int = Form(None),
#                                 task_id: int = Form(None),
#                                 page: int = 1,
#                                 size: int = 50
# ):
#     user = get_user_token(db,token=token)
#     if not user:
#         return {"status":0,"msg":"Your login session expires.Please login again."}
    
#     if user.user_type == 3:
#         get_projects = db.query(StudentProjectDetail).filter(StudentProjectDetail.status==1,StudentProjectDetail.user_id==user.id)
#     else:
#         batch = db.query(Batch).filter(Batch.status==1).all()
#         batch_ids = [data.id for data in batch]
#         if not batch:
#             return {"status":0,"msg":"None of the batches are active"}
     
#         get_projects = db.query(StudentProjectDetail).join(
#             User, User.id == StudentProjectDetail.user_id
#         ).outerjoin(
#             Score,
#             Score.student_project_id == StudentProjectDetail.id
#         ).filter(User.batch_id.in_(batch_ids),StudentProjectDetail.status == 1,Score.id.is_(None))

#     if course_id:
#             get_projects = get_projects.filter(User.course_id==course_id)
        
#     if task_id:
#         get_projects = get_projects.filter(StudentProjectDetail.task_id == task_id)

#     get_project_count = get_projects.count()
#     totalPages,offset,limit = get_pagination(get_project_count,page,size)
#     get_projects = get_projects.order_by(StudentProjectDetail.id.desc()).limit(limit).offset(offset).all()

#     data_list = []

#     for project in get_projects:
#         data_list.append({
#             "id": project.id,
#             "project_start_date": project.project_start_date.strftime("%Y-%m-%d %H:%M"),
#             "project_end_date": project.project_end_date.strftime("%Y-%m-%d %H:%M"),
#             "description": project.description,
#             "task_id": project.task_id,
#             "task": project.task.name,
#             "student_id": project.user_id,
#             "user_name": project.student.username,
#             "name": project.student.name.capitalize(),
#             "project" : f"{settings.BASEURL}/{project.project_url}",
#             # "course": project.student.course.name if project.student.course else None,
#             # "course_id": project.task.course ,
#             "created_at": project.created_at
#         })

#     data=({"page":page,
#            "size":size,
#            "total_page":totalPages,
#            "total_count":get_project_count,
#            "items":data_list})
            
#     return ({"status":1,"msg":"Success.","data":data})


@router.post("/list_student_project")
async def listStudentProject(
                                db: Session = Depends(get_db),
                                token: str = Form(...),
                                course_id: int = Form(None),
                                task_id: int = Form(None),
                                page: int = 1,
                                size: int = 50
):
    user = get_user_token(db, token=token)
    if not user:
        return {"status": 0, "msg": "Your login session expires. Please login again."}

    if user.user_type == 3:
        get_projects = db.query(StudentProjectDetail).filter(
            StudentProjectDetail.status == 1,
            StudentProjectDetail.student_id == user.id
        )
    else:
        batch = db.query(Batch).filter(Batch.status == 1).all()
        batch_ids = [data.id for data in batch]
        if not batch:
            return {"status": 0, "msg": "None of the batches are active"}

        # Join with CourseAssign table to filter by course_id
        get_projects = db.query(StudentProjectDetail).join(
            User, User.id == StudentProjectDetail.student_id
        ).outerjoin(
            Score, Score.student_project_id == StudentProjectDetail.id
        ).filter(
            User.batch_id.in_(batch_ids),
            StudentProjectDetail.status == 1,
            Score.id.is_(None)
        ).distinct(StudentProjectDetail.id)
    if user.user_type==2:
        get_projects=get_projects.join(
            CourseAssign, CourseAssign.user_id == User.id  # Join CourseAssign table
        ).filter(CourseAssign.status==1)
    # Filter by course_id if provided
    if course_id:
        get_projects = get_projects.filter(CourseAssign.course_id == course_id,CourseAssign.status==1)
    
    if task_id:
        get_projects = get_projects.filter(StudentProjectDetail.task_id == task_id)

    get_project_count = get_projects.count()
    totalPages, offset, limit = get_pagination(get_project_count, page, size)
    get_projects = get_projects.order_by(StudentProjectDetail.id.desc()).limit(limit).offset(offset).all()

    data_list = []

    for project in get_projects:
        data_list.append({
            "id": project.id,
            "project_start_date": project.project_start_date.strftime("%Y-%m-%d %H:%M"),
            "project_end_date": project.project_end_date.strftime("%Y-%m-%d %H:%M"),
            "description": project.description,
            "task_id": project.task_id,
            "task": project.task.name,
            "student_id": project.student_id,
            "user_name": project.student.username,
            "name": project.student.name.capitalize(),
            "project": f"{settings.BASEURL}/{project.project_url}",
            "created_at": project.created_at,
            "updated_at":project.updated_at,
        })

    data = {
        "page": page,
        "size": size,
        "total_page": totalPages,
        "total_count": get_project_count,
        "items": data_list
    }

    return {"status": 1, "msg": "Success.", "data": data}



@router.post("/update_project")
async def updateProject(
                            db: Session = Depends(get_db),
                            token: str = Form(...),
                            project_id: int = Form(...),
                            project_start_date: datetime = Form(...),
                            project_end_date: datetime = Form(...),
                            description: str = Form(None),
                            project_url: UploadFile = File(None),
                            task_id: int = Form(...)
):
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}

    get_project = db.query(StudentProjectDetail).filter(
        StudentProjectDetail.id == project_id,StudentProjectDetail.status==1
    ).first()
    if not get_project:
        return {"status":0,"msg":"Project not found"}
    if user.user_type ==3:
        get_score = db.query(Score).filter(Score.task_id==task_id,Score.student_id==user.id,Score.status==1,Score.mark != None).first()
        if get_score:
            return {"status":0,"msg":"project has already been marked and cannot be edited."}
        # if get_project.is_marked ==1:
        #     return {"status":0,"msg":"project has already been marked and cannot be edited."}
    if project_url:
        file_path, file_url = file_storage(project_url, project_url.filename)
        get_project.project_url=file_url
    if description:
        get_project.description = description

    get_project.project_start_date = project_start_date
    get_project.project_end_date = project_end_date
    get_project.task_id = task_id
    db.commit()
    return {"status":1, "msg":"Successfully project updateted"}

@router.post("/delete_project")
async def deleteProject(
                            db: Session = Depends(get_db),
                            token: str = Form(...),
                            project_id: int = Form(...)
):
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    get_project = db.query(StudentProjectDetail).filter(
        StudentProjectDetail.id == project_id,StudentProjectDetail.status==1
    ).first()

    if not get_project:
        return {"status":0,"msg":"Project not found"}
    if user.user_type ==3:
        get_score = db.query(Score).filter(Score.task_id==get_project.task_id,Score.student_id==user.id,Score.status==1,Score.mark != None).first()
        if get_score:
            return {"status":0,"msg":"project has already been marked and cannot be edited."}
    get_project.status = -1
    db.commit()
    return {"status":1,"msg":"Project successfully deleted"}


        
