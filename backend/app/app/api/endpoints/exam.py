from fastapi import APIRouter,Form,Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api.deps import *
from datetime import datetime
from app.core.config import settings
from app.utils import *
import random
from app.schemas import GetAnswer
from fastapi.encoders import jsonable_encoder


router = APIRouter()

@router.post("/create_exam")
async def createExam(
                        db: Session = Depends(get_db),
                        token: str = Form(...),
                        name: str = Form(...),
):
        user = get_user_token(db=db,token=token)
        if not user:
            return {"status":0,"msg":"Your login session expires.Please login again."}
        if user.user_type not in [1,2]:
              return {"status":0, "msg":"Access denied"}
        create_exam = Exam(
              name = name,
              status = 1,
              created_at = datetime.now(settings.tz_IN),
              updated_at = datetime.now(settings.tz_IN),
        )
        db.add(create_exam)
        db.commit()
        return {"status":1, "msg":"Exam created successfully"}

@router.post("/list_exam")
async def listExam(
                    db: Session = Depends(get_db),
                    token: str = Form(...),
                    exam_id: int = Form(None),
                    name: str = Form(None),
                    page: int = 1,
                    size: int = 50
):
        user = get_user_token(db=db,token=token)
        if not user:
            return {"status":0,"msg":"Your login session expires.Please login again."}
        if user.user_type not in [1,2]:
              return {"status":0, "msg":"Access denied"}
        get_exam = db.query(Exam).filter(Exam.status == 1)
        if exam_id:
              get_exam = get_exam.filter(Exam.id == exam_id)
        if name:
              get_exam = get_exam.filter(Exam.name.ilike(f"%{name}%"))

        get_exam = get_exam.order_by(Exam.name)
        totalCount= get_exam.count()
        total_page,offset,limit=get_pagination(totalCount,page,size)
        get_exam=get_exam.limit(limit).offset(offset).all()
        dataList =[]
    
        for row in get_exam:
                dataList.append({
                    "exam_id" :row.id,
                    "exam_name":row.name.capitalize(),
                    "created_at":row.created_at,
                
                })
        data=({"page":page,"size":size,"total_page":total_page,
                    "total_count":totalCount,
                    "items":dataList})
        return {"status":1,"msg":"Success","data":data}

@router.post("/update_exam")
async def updateExam(
                        db: Session = Depends(get_db),
                        token: str = Form(...),
                        exam_id: int = Form(...),
                        name: str = Form(...)
):
        
        user = get_user_token(db=db,token=token)
        if not user:
            return {"status":0,"msg":"Your login session expires.Please login again."}
        if user.user_type not in [1,2]:
              return {"status":0, "msg":"Access denied"}
        
        get_exam = db.query(Exam).filter(Exam.id ==exam_id, Exam.status == 1).first()

        if not get_exam:
              return {"status": 0, "msg": "Exam not found"}
        
        get_exam.name = name
        get_exam.updated_at = datetime.now(settings.tz_IN)
        db.commit()
        return {"status": 1, "msg": "Exam updated successfully"}

@router.post("/assign_exam")
async def assignExam(
                        db: Session = Depends(get_db),
                        token: str = Form(...),
                        batch_id: int = Form(...),
                        exam_id: int = Form(...),
                        course_id: int = Form(None),
):
        user = get_user_token(db=db,token=token)
        if not user:
            return {"status":0,"msg":"Your login session expires.Please login again."}
        if user.user_type not in [1,2]:
              return {"status":0, "msg":"Access denied"}
        """
        # check given batch is correct
        """
        get_batch = db.query(Batch).filter(Batch.id == batch_id).first()
        if not get_batch:
              return {"status":0,"msg":"Batch not found"}
        """
        # check given exam is correct
        """
        get_exam = db.query(Exam).filter(Exam.id == exam_id, Exam.status == 1).first()
        if not get_exam:
              return {"status":0, "msg":"Invalid exam details"}
        """
        # The exam has more than one set of papers, so students don't share the same question paper
        # before the exam is assigned.
        # Check if each set contains questions.
        # Ensure that each set has the same total marks, so the score of each student is consistent.
        """
        # check exam has paper
        get_set_ids = []
        if not get_exam.sets:
              return {"status":0, "msg":"There is no question paper for this specific Exam"}
        
        for set in get_exam.sets:
              get_set_ids.append(set.id)
        # Get total for all set of papers
        sumof_all_paper_marks = db.query(func.sum(Question.mark)).filter(Question.set_id.in_(get_set_ids)).group_by(Question.set_id).all()

        if len(sumof_all_paper_marks) != len(get_set_ids):
              return {"status":0, "msg":"Some set of paper has no questions"}
        # convert decimal to int
        list_of_all_set_marks = []
        for mark in sumof_all_paper_marks:
              list_of_all_set_marks.append(int(mark[0]))
        # check each set total mark is same    
        for mark in list_of_all_set_marks:
              if list_of_all_set_marks[0]!=mark:
                    return {"status":0, "msg":"Question papers total marks are not same"}

        # Get students in active batch
        get_students = db.query(User).filter(User.user_type == 3, User.status == 1,User.batch_id==batch_id)
        # check given course id is valid
        if course_id:
              get_course = db.query(Course).filter(Course.id == course_id, Course.status == 1).first()
              if not get_course:
                    return {"status":0, "msg": "Course not found"}
              get_students = get_students.filter(User.course_id == course_id)

        get_students = get_students.all()
        for student in get_students:
              assign = AssignExam(
                    batch_id = batch_id,
                    exam_id = exam_id,
                    course_id = course_id,
                    student_id = student.id,
                    set_id = random.choice(get_set_ids),
                    status = 1,
                    created_at = datetime.now(settings.tz_IN),
                    updated_at = datetime.now(settings.tz_IN)
              )
              db.add(assign)
        db.commit()
        return {"status": 1, "status": "Exam assigned successfully"}

@router.post("/list_student_exam")
async def listStudentExam(
                              db: Session = Depends(get_db),
                              token: str = Form(...),
                              # ba  
                              page: int = 1,
                              size: int = 50
):
      user = get_user_token(db=db,token=token)
      if not user:
            return {"status":0,"msg":"Your login session expires.Please login again."}
      
      get_assigned = db.query(AssignExam).filter(AssignExam.student_id == user.id).order_by(AssignExam.id)
      totalCount= get_assigned.count()
      total_page,offset,limit=get_pagination(totalCount,page,size)
      get_assigned=get_assigned.limit(limit).offset(offset).all()
      dataList =[]

      for data in get_assigned:
            dataList.append({
                  "user_id": user.id,
                  "exam_id": data.exam_id,
                  "exam_name": data.exam.name,
                  "set_id": data.set_id,
                  "set_name": data.set.name
                  # ""
            })
      data=({"page":page,"size":size,"total_page":total_page,
                    "total_count":totalCount,
                    "items":dataList})
      return {"status":1,"msg":"Success","data":data}



@router.post("/Answer")
async def Answer(base:GetAnswer,db:Session=Depends(get_db),
                    ):
      base=jsonable_encoder(base)
      token=base["token"]
      assign_exam_id=base["assign_exam_id"]
      user=get_user_token(db=db,token=token)
   
#     
      if not user:
         return {"status":0,"msg":"Your login session expires.Please login again."}
    
#     if user.userType==1 or 2:
      for row in base["question_information"]:
            question_id=row["question_id"]
            type_id=row["type_id"]
            answer_id=row["answer_id"]
            answer=row["answer"]
            print(question_id,type_id,answer_id,answer)
           
            add_new=StudentExamDetail(
                  question_id=question_id,
                  
                  answer=answer,
                  type__id=type_id,
                  student_id=user.id,
                  assign_exam_id=assign_exam_id,
                  status=1,
                  created_at=datetime.now())
            db.add(add_new)
            db.commit()
            print(answer_id,11111111)
            for answer in answer_id:
                  print(answer,333333)
                  add_ExamInformarion=ExamInformarion(
                        StudentExamDetail_id=add_new.id,
                        answer_id=answer,
                        status=1,
                        created_at=datetime.now()
                  )
                  db.add(add_ExamInformarion)
                  db.commit()
      return {"status":1,"msg":"Success"}


# @router.post("/exam_result")
# async def exam_result(
#                               db: Session = Depends(get_db),
#                               token: str = Form(...),
#                               # ba  
#                               user_id: int = Form(...),
#                               exam_id: int = Form(...)
# ):
#       user = get_user_token(db=db,token=token)
#       if not user:
#             return {"status":0,"msg":"Your login session expires.Please login again."}
#       getdata=db.query(StudentExamDetail,ExamInformarion,Option)\
#             .join(StudentExamDetail,StudentExamDetail.id==ExamInformarion.StudentExamDetail_id)\
#             .join(Option,Option.id==ExamInformarion.answer_id)\
#             .filter(StudentExamDetail.student_id==1).all()
      
