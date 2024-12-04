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
                        task_id: int = Form(...),
                        student_id: int = Form(...),
                        mark: int = Form(...),
                        description: str = Form(None)
):
    user = get_user_token(db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    
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
    return {"status":1,"msg":"Score entered successfully"}

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
    
    get_student_score = db.query(Score).filter(Score.student_id==student_id,Score.status==1)

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
            "student_name":data.student.name,
            "mark_giver_id": data.teacher_id,
            "mark_giver_name":data.teacher.name,
            "created_at":data.created_at.strftime("%Y-%m-%d"),
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
