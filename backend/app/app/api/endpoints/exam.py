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
                    "no_of_set":len(row.sets)
                
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
        sumof_all_paper_marks = db.query(func.sum(Question.mark)).filter(Question.set_id.in_(get_set_ids),Question.status==1).group_by(Question.set_id).all()

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
        return {"status": 1, "msg": "Exam assigned successfully"}

@router.post("/list_student_exam")
async def listStudentExam(
                              db: Session = Depends(get_db),
                              token: str = Form(...),
                              # batch_id: int = Form(None),
                              student_id: int = Form(None),
                              exam_id: int = Form(None),
                              course_id: int = Form(None), 
                              page: int = 1,
                              size: int = 50
):
      user = get_user_token(db=db,token=token)
      if not user:
            return {"status":0,"msg":"Your login session expires.Please login again."}
      
      batch = db.query(Batch).filter(Batch.status==1).first()
      if not batch:
            return {"status":0,"msg":"None of the batches are active"}
      get_assigned_details = db.query(AssignExam).filter(AssignExam.status == 1, AssignExam.batch_id == batch.id)
      # if user.user_type in [1,2]:
      #       get_assigned_details = get_assigned_details
      if user.user_type == 3:
            # get_assigned_details = get_assigned_details.filter(AssignExam.student_id == user.id)
            get_assigned_details = get_assigned_details.outerjoin(
                  StudentExamDetail, StudentExamDetail.assign_exam_id == AssignExam.id
                  ).filter(
                  AssignExam.student_id == user.id,
                  StudentExamDetail.assign_exam_id == None
                  )
      # if batch_id:
      if student_id:
            get_assigned_details = get_assigned_details.filter(
                  AssignExam.student_id == student_id
            )
      if exam_id:
            get_assigned_details = get_assigned_details.filter(
                  AssignExam.exam_id == exam_id
            )
      if course_id:
            get_assigned_details = get_assigned_details.filter(
                  AssignExam.course_id == course_id
            )

      totalCount= get_assigned_details.count()
      total_page,offset,limit=get_pagination(totalCount,page,size)
      get_assigned_details=get_assigned_details.order_by(AssignExam.id.desc()).limit(limit).offset(offset).all()
      dataList =[]

      for data in get_assigned_details:
            total_mark = (
        sum(detail.mark for detail in data.exam_details if detail.mark is not None)
        if data.exam_details else None
    )
            dataList.append({
                  "user_id": user.id,
                  "exam_id": data.exam_id,
                  "exam_name": data.exam.name,
                  "set_id": data.set_id,
                  "set_name": data.set.name,
                  "created_at": data.created_at,
                  "attended_at": data.exam_details[0].created_at if data.exam_details else None,
                  "assigned_id": data.id,
                  "student_id": data.student_id,
                  "student_name": data.student.name,
                  "student_user_name": data.student.username,
                  "total_mark": total_mark
 
            })
      data=({"page":page,"size":size,"total_page":total_page,
                    "total_count":totalCount,
                    "items":dataList})
      return {"status":1,"msg":"Success","data":data}



@router.post("/answer")
async def answer(
                  base:GetAnswer,
                  db:Session=Depends(get_db),
):    
      base=jsonable_encoder(base)
      token=base["token"]
      user=get_user_token(db=db,token=token)
      if not user:
         return {"status":0,"msg":"Your login session expires.Please login again."}

      assign_exam_id=base["assign_exam_id"]
      get_assigned = db.query(AssignExam).filter(AssignExam.id == assign_exam_id).first()
      if not get_assigned:
            return{"status":0, "msg":"Invaild assigned id"}
      get_assigned_exam = db.query(StudentExamDetail).filter(StudentExamDetail.assign_exam_id == assign_exam_id).first()
      if get_assigned_exam:
            return {"status":0, "msg":"You already taken this test"}

      get_set = db.query(Set).filter(Set.id == get_assigned.set_id).first()
      if len(get_set.questions) != len(base["question_information"]):
            return {"status":0 , "msg": "Please answer all questions"}

      # if not base["question_information"]:
      #       return {"nil"}
      for row in base["question_information"]:
            question_id=row["question_id"]
            type_id=row["type_id"]
            answer_id=row["answer_id"]
            answer=row["answer"]
            option = ""

            for i in answer_id:
                  if option == "":
                        option = str(i)
                  else:
                        option = option + "," + str(i)

            get_answers = db.query(Option).filter(Option.question_id == question_id,Option.answer_status == 1).all()
            get_question = db.query(Question).filter(Question.id == question_id).first()
            get_question_mark = get_question.mark
            get_answer_ids = [option.id for option in get_answers]

            mark_status = None
            if sorted(answer_id) == sorted(get_answer_ids):
                  mark_status = get_question_mark
            elif type_id == 2:
                  print(get_question.answer, answer)
                  if get_question.answer and get_question.answer.strip().lower() == answer.strip().lower():
                        mark_status = get_question_mark

            add_new=StudentExamDetail(
                  question_id=question_id,
                  option_ids = option,
                  answer=answer,
                  type__id=type_id,
                  student_id=user.id,
                  assign_exam_id=assign_exam_id,
                  status=1,
                  created_at=datetime.now(),
                  mark=mark_status
                  )
            db.add(add_new)
            db.commit()
      # get_total = db.query(func.sum(StudentExamDetail.mark)).group_by(StudentExamDetail.assign_exam_id).scalar()
      # print(get_total,"score")
      return {"status":1,"msg":"Success"}

@router.post("/get_student_exam_details")
async def getStudentExamDetails(
                                    db: Session = Depends(get_db),
                                    token: str = Form(...),
                                    assigned_id: int = Form(...),
                                    page: int = 1,
                                    size: int = 50
):
      user=get_user_token(db=db,token=token)
      if not user:
         return {"status":0,"msg":"Your login session expires.Please login again."}
      if user.user_type not in [1,2]:
              return {"status":0, "msg":"Access denied"}
      
      get_assigned_details = db.query(AssignExam).filter(AssignExam.id == assigned_id).first()
      if not get_assigned_details:
            return {"status":0, "msg":"Invaild details"}
      
      get_student_details = db.query(StudentExamDetail).filter(StudentExamDetail.assign_exam_id == assigned_id)
      if not get_student_details:
            return {"status":0, "msg": "Invaild details"}
      get_set = db.query(Set).filter(Set.id == get_assigned_details.set_id, Set.status == 1).first()
      if not get_set:
            return {"status":0, "msg":"Invaild details"}
      total_mark_for_set = sum(question.mark for question in get_set.questions)
      print(total_mark_for_set)

      totalCount= get_student_details.count()
      total_page,offset,limit=get_pagination(totalCount,page,size)
      get_student_details=get_student_details.order_by(StudentExamDetail.id).limit(limit).offset(offset).all()
      data_list = []
      student_score = 0
      for data in get_student_details:
            if data.option_ids:
                  options = [int(option) for option in data.option_ids.split(",")]
                  get_options = db.query(Option).filter(Option.id.in_(options)).all()
                  
            data_list.append({
                  "student_exam_detail_id": data.id,
                  "type_id": data.type__id,
                  "question": data.question.question_title,
                  "options": [title.name for title in get_options] if data.option_ids else None,
                  "answer": data.answer,
                  "actual_mark": data.mark,
                  "question_mark": data.question.mark
            })
            if data.mark:
                  student_score+=data.mark
      data=({"page":page,"size":size,"total_page":total_page,
                    "total_count":totalCount,
                    "total_mark_for_this_exam":total_mark_for_set,
                    "student_score":student_score,
                    "items":data_list})
      return {"status":1,"msg":"Success","data":data}
      # return {"status":0, "msg":data_list}

@router.post("/edit_paragraph_mark")
async def editParagraphMark(
                              db: Session = Depends(get_db),
                              token: str = Form(...),
                              student_exam_detail_id: int = Form(...),
                              mark: int = Form(...)
):
      user=get_user_token(db=db,token=token)
      if not user:
         return {"status":0,"msg":"Your login session expires.Please login again."}
      if user.user_type not in [1,2]:
            return {"status":0, "msg":"Access denied"}
      
      get_student_exam_detail = db.query(StudentExamDetail).filter(StudentExamDetail.id == student_exam_detail_id).first()
      if not get_student_exam_detail:
            return {"status":0 ,"msg":"Invaild student record"}
      get_question_mark = get_student_exam_detail.question.mark
      if mark > get_question_mark:
            return {"status": 0, "msg":f"Maximum mark is {get_question_mark}"}
      
      get_student_exam_detail.mark = mark
      db.commit()
      return {"status":1, "msg":"Mark updeted successfully"}
            


      
