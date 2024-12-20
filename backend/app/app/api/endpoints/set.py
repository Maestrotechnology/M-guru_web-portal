from fastapi import APIRouter,Depends,Form
from sqlalchemy.orm import Session
from utils import *
from app.api.deps import *

router = APIRouter()

@router.post("/create_set")
async def createSet(
                        db: Session = Depends(get_db),
                        token: str = Form(...),
                        set_name: str = Form(...),
                        exam_id: int = Form(...)
):
        user = get_user_token(db=db,token=token)
        if not user:
            return {"status":0,"msg":"Your login session expires.Please login again."}
        if user.user_type not in [1,2]:
              return {"status":0, "msg":"Access denied"}
        
        get_exam = db.query(Exam).filter(Exam.id == exam_id, Exam.status == 1).first()
        if not get_exam:
              return {"status":0, "msg": "Exam not found"}
        
        create_set = Set(
              name = set_name,
              exam_id = exam_id,
              status = 1,
              created_at = datetime.now(settings.tz_IN),
              updated_at = datetime.now(settings.tz_IN)
        )
        db.add(create_set)
        db.commit()
        return {"status":1, "msg":"set created successfully"}

@router.post("/list_set")
async def listSet(
                    db: Session = Depends(get_db),
                    token: str = Form(...),
                    exam_id: int = Form(...),
                    set_id: int = Form(None),
                    name: str = Form(None),
                    page: int = 1,
                    size: int = 50
):
        user = get_user_token(db=db,token=token)
        if not user:
            return {"status":0,"msg":"Your login session expires.Please login again."}
        if user.user_type not in [1,2]:
              return {"status":0, "msg":"Access denied"}
        
        get_set = db.query(Set).filter(Set.exam_id==exam_id,Set.status==1)

        if set_id:
              get_set = get_set.filter(Set.id == set_id)
        if name:
              get_set = get_set.filter(Set.name.ilike(f"%{name}%"))

        get_set = get_set.order_by(Set.id)
        totalCount= get_set.count()
        total_page,offset,limit=get_pagination(totalCount,page,size)
        get_set=get_set.limit(limit).offset(offset).all()
        dataList =[]
    
        for row in get_set:
                dataList.append({
                    "set_id" :row.id,
                    "set_name":row.name.capitalize(),
                    "exam_id":row.exam_id,
                    "created_at":row.created_at,
                    "no_of_questions":len([question for question in row.questions if question.status == 1]) if row.questions else None,
                    "total": sum(question.mark for question in row.questions if question.status == 1) if row.questions else None
                })
        data=({"page":page,"size":size,"total_page":total_page,
                    "total_count":totalCount,
                    "items":dataList})
        return {"status":1,"msg":"Success","data":data}

@router.post("/update_set")
async def updateSet(
                        db: Session = Depends(get_db),
                        token: str = Form(...),
                        set_name: str = Form(...),
                        set_id: int = Form(...)
):
      user = get_user_token(db=db,token=token)
      if not user:
          return {"status":0,"msg":"Your login session expires.Please login again."}
      if user.user_type not in [1,2]:
              return {"status":0, "msg":"Access denied"}
      
      get_set = db.query(Set).filter(Set.id == set_id, Set.status == 1).first()
      if not get_set:
            return {"status":0, "msg":"Invaild set"}
      
      get_set.name = set_name
      db.commit()
      return {"status": 1, "msg":"Set successfully updated"}

@router.post("/delete_update")
async def deleteUpdate(
                        db: Session = Depends(get_db),
                        token: str = Form(...),
                        set_id: int = Form(...)
):
      user = get_user_token(db=db,token=token)
      if not user:
          return {"status":0,"msg":"Your login session expires.Please login again."}
      if user.user_type not in [1,2]:
              return {"status":0, "msg":"Access denied"}
      
      get_set = db.query(Set).filter(Set.id == set_id, Set.status == 1).first()
      if not get_set:
            return {"status":0, "msg":"Invaild set"}
      
      get_set.status = -1
      db.commit()
      return {"status":1, "msg": "Set Successfully deleted"}
      
