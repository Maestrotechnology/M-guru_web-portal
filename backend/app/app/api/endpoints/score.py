from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.models import *
from app.core.config import settings
from datetime import datetime
from app.utils import *
from api.deps import get_db,get_user_token

router = APIRouter()

@router.post("/enter_score")
async def enterScore(
                        db:Session=Depends(get_db),
                        token:str = Form(...),
                        task_id: int = Form(None),
                        student_ids: str = Form(),
                        mark: str = Form(...),
                        task_name: str = Form(None),
                        description: str = Form(None),
                        project_ids: str = Form(None),
                        task_ids: str = Form(None)
):
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    if task_id:
        get_task = db.query(Task).filter(Task.id == task_id, Task.status == 1).first()

        if not get_task:
            return {"status":0, "msg": "Task not found"}
    student_ids = student_ids.split(",")
    # get_students = db.query(User).filter(User.)
    if project_ids and task_ids:
        project_ids = project_ids.split(",")
        task_ids = task_ids.split(",")

        for index in range(len(student_ids)):
            create_score = Score(
                    description = description,
                    status = 1,
                    created_at = datetime.now(settings.tz_IN),
                    updated_at = datetime.now(settings.tz_IN),
                    mark = mark,
                    task_id = task_ids[index],
                    student_id = student_ids[index],
                    teacher_id = user.id,
                    student_project_id = project_ids[index],
                )
            db.add(create_score)
            db.commit()
        return {"status":1,"msg":"Score entered successfully"}
    
    for index in range(len(student_ids)):
        create_score = Score(
                description = description,
                status = 1,
                created_at = datetime.now(settings.tz_IN),
                updated_at = datetime.now(settings.tz_IN),
                mark = mark,
                task_id = task_id,
                student_id = student_ids[index],
                teacher_id = user.id,
                # student_project_id = project_ids[index] if project_ids else None
            )
        db.add(create_score)
        db.commit()
    return {"status":1,"msg":"Score entered successfully"}
    

    # if user.user_type not in [1,2]:
    #     return {"status":0,"msg":"Access denied"}
    # create_task = None
    # if not task_ids and not task_name:
    #     return {"status":0, "msg":"Task Required"}
    
    # get_students_ids = student_ids.split(",")
    # get_marks = marks.split(",")
    # if len(get_students_ids)!=len(get_marks):
    #     return {"status":0, "msg":"Invaild details"}
    
    # if task_ids and project_ids:
    #     get_task_ids = task_ids.split(",")
    #     get_project_ids = project_ids.split(",")
    #     if len(get_students_ids)!=len(get_marks) and len(get_task_ids)!=len(get_students_ids) and len(get_marks)!=len(get_task_ids):
    #         return {"status":0, "msg":"Invaild details"}
        
    #     for index in range(len(get_students_ids)):
    #         create_score = Score(
    #             description = description,
    #             status = 1,
    #             created_at = datetime.now(settings.tz_IN),
    #             updated_at = datetime.now(settings.tz_IN),
    #             mark = get_marks[index],
    #             task_id = get_task_ids[index],
    #             student_id = get_students_ids[index],
    #             teacher_id = user.id,
    #             student_project_id = get_project_ids[index]
    #         )
    #         db.add(create_score)
    #     db.commit()
    #     return {"status":1,"msg":"Score entered successfully"}

    # if task_name:
    #     create_task = Task(
    #         name=task_name,
    #         status=1,
    #         created_by_user_id=user.id,
    #         description=description
    #     )
    #     db.add(create_task)
    #     db.commit()
                                  

    # for index in range(len(get_students_ids)):
    #     create_score = Score(
    #         description = description,
    #         status = 1,
    #         created_at = datetime.now(settings.tz_IN),
    #         updated_at = datetime.now(settings.tz_IN),
    #         mark = get_marks[index],
    #         task_id = create_task.id,
    #         student_id = get_students_ids[index],
    #         teacher_id = user.id
    #     )
    #     db.add(create_score)
    # db.commit()
    # return {"status":1,"msg":"Score entered successfully"}

@router.post("/list_score")
async def listScore(
                     db:Session=Depends(get_db),
                     token:str = Form(...),
                     score_id: int = Form(None),
                     task_id: int = Form(None),
                     student_id: int = Form(...),
                     page: int = Form(1),
                     size: int = Form(10)
):
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    get_student_score = db.query(Score).join(Task,Task.id == Score.task_id).filter(Score.student_id==student_id,Score.status==1,Task.status == 1)

    if task_id:
        get_student_score = get_student_score.filter(Score.task_id==task_id)

    if score_id:
        get_student_score = get_student_score.filter(Score.id==score_id)

    get_student_score = get_student_score.order_by(Score.id)
    totalCount = get_student_score.count()
    total_page,offset,limit=get_pagination(totalCount,page,size)
    get_student_score=get_student_score.limit(limit).offset(offset).all()

    data_list = []
    for data in get_student_score:
        data_list.append({
            "id":data.id,
            "mark":data.mark,
            "task_id":data.task_id,
            "task_name":data.task.name,
            "student_id":data.student_id,
            "student_name":data.student.name.capitalize(),
            "mark_giver_id": data.teacher_id,
            "mark_giver_name":data.teacher.name,
            "created_at":data.created_at.strftime("%d-%m-%Y"),
            "description":data.description
        })
    data=({"page":page,"size":size,"total_page":total_page,
                "total_count":totalCount,
                "items":data_list})
    return {"status":1,"msg":"Success","data":data}

@router.post("/update_score")
async def updateScore(
                        db: Session = Depends(get_db),
                        token: str = Form(...),
                        score_id: int = Form(...),
                        mark: int = Form(...),
                        description: str = Form(None)
):
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    get_student_score = db.query(Score).filter(Score.id==score_id,Score.status==1).first()

    if not get_student_score:
        return {"status":0,"msg":"Score not found"}
    
    if description:
        get_student_score.description=description
    else:
        get_student_score.description=None
        
    get_student_score.updated_at=datetime.now(settings.tz_IN)
    get_student_score.mark = mark
    db.commit()
    return {"status":1,"msg":"Score successfully updated"}

@router.post("/delete_score")
async def deleteScore(
                        db: Session = Depends(get_db),
                        token: str = Form(...),
                        score_id: int = Form(...)
):
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
    get_student_score = db.query(Score).filter(Score.id == score_id, Score.status==1).first()

    if not get_student_score:
        return {"status":0,"msg":"Score not found"}
    
    get_student_score.status=-1
    db.commit()
    return {"status":1,"msg":"Score successfully deleted"}

@router.post("/enter_induvial_score")
async def enterInduvialScore(
                                db:Session=Depends(get_db),
                        token:str = Form(...),
                        task_id: str = Form(...),
                        student_id: str = Form(...),
                        mark: str = Form(...),
                        description: str = Form(None)
):
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    if user.user_type not in [1,2]:
        return {"status":0,"msg":"Access denied"}

    get_task = db.query(Task).filter(Task.status==1,Task.id==task_id).first()
    get_student = db.query(User).filter(User.id == student_id, User.status == 1).first()
    if not get_task:
        return {"status":0, "msg": "Invaild task"}
    if not get_student:
        return {"status":0, "msg": "Student not found"}
    
    create_score = Score(
            description = description,
            status = 1,
            created_at = datetime.now(settings.tz_IN),
            updated_at = datetime.now(settings.tz_IN),
            mark = mark,
            task_id = task_id,
            student_id = student_id,
            teacher_id = user.id
        )
    db.add(create_score)
    db.commit()
    return {"status":1, "msg": "Score entered successfully"}
    
    
    

    

