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
                set_counts = db.query(Set).filter(Set.status ==1,Set.exam_id==row.id).count()
                dataList.append({
                    "exam_id" :row.id,
                    "exam_name":row.name.capitalize(),
                    "created_at":row.created_at,
                    "no_of_set":set_counts
                
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
              if set.status ==1:
                  get_set_ids.append(set.id)
        # Get total for all set of papers
        sumof_all_paper_marks = db.query(func.sum(Question.mark)).filter(Question.set_id.in_(get_set_ids),Question.status==1).group_by(Question.set_id).all()
        print(sumof_all_paper_marks,get_set_ids)
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
      
      batch = db.query(Batch).filter(Batch.status==1).all()
      batch_ids = [data.id for data in batch]
      if not batch:
            return {"status":0,"msg":"None of the batches are active"}
      get_assigned_details = db.query(AssignExam).filter(AssignExam.status == 1, AssignExam.batch_id.in_(batch_ids))
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
            print(get_assigned_details.count(),1111111111)
      # if batch_id:
      if student_id:
            get_assigned_details = get_assigned_details.filter(
                  AssignExam.student_id == student_id
            )
      if exam_id:
            get_assigned_details = get_assigned_details.filter(
                  AssignExam.exam_id == exam_id
            )
      print("-----------------------------")
      print(course_id)
      print(get_assigned_details.count(),22222222)

      if course_id:
            get_assigned_details = get_assigned_details.filter(
                  AssignExam.course_id == course_id
            )
            print(get_assigned_details.count())
      totalCount= get_assigned_details.count()
      print(get_assigned_details.count(),33333333)
      total_page,offset,limit=get_pagination(totalCount,page,size)
      get_assigned_details=get_assigned_details.order_by(AssignExam.id.desc()).limit(limit).offset(offset).all()
      dataList =[]

      for data in get_assigned_details:
            total_mark = (
                              sum(detail.mark for detail in data.exam_details if detail.mark is not None)
                              if data.exam_details else None
                          )
            if data.set.questions:
                  no_of_question = sum(1 for qus in data.set.questions if qus.status == 1)

            dataList.append({
                  "user_id": user.id,
                  "exam_id": data.exam_id,
                  "exam_name": data.exam.name,
                  "set_id": data.set_id,
                  "set_name": data.set.name,
                  "course": data.course.name if data.course else None,
                  "created_at": data.created_at,
                  "attended_at": data.exam_details[0].created_at if data.exam_details else None,
                  "assigned_id": data.id,
                  "student_id": data.student_id,
                  "student_name": data.student.name,
                  "student_user_name": data.student.username,
                  "total_mark": total_mark,
                  "no_of_question": no_of_question
 
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
      get_question_information = base.question_information
      token = base.token
      assigned_id = base.assign_exam_id
      question_id = get_question_information.question_id
      type_id = get_question_information.type_id
      answer_id = get_question_information.answer_id
      answer = get_question_information.answer
      # exam_status = base.completed
      
      user=get_user_token(db=db,token=token)
      if not user:
         return {"status":0,"msg":"Your login session expires.Please login again."}

      get_assigned = db.query(AssignExam).filter(AssignExam.id == assigned_id).first()
      if not get_assigned:
            return{"status":0, "msg":"Invaild assigned id"}
      get_question = db.query(Question).filter(Question.id == question_id,Question.status == 1).first()
      if not get_question:
            return{"status":0, "msg":"Invaild question"}
      get_question_mark = get_question.mark
      get_type = db.query(TypeOfQuestion).filter(TypeOfQuestion.id == type_id,TypeOfQuestion.status == 1).first()
      if not get_type:
            return{"status":0, "msg":"Invaild type of question"}
      get_answers = db.query(Option).filter(Option.question_id == question_id,Option.answer_status == 1).all()
      get_answer_ids = [option.id for option in get_answers]
      option = ""
      if answer_id:
            for i in answer_id:
                  if option == "":
                        option = str(i)
                  else:
                        option = option + "," + str(i)
      scored_mark = 0
      print(answer_id,"----")
      if type_id==2:
            if answer.strip().lower() == get_question.answer.strip().lower():
                  scored_mark = get_question_mark
      elif type_id in [1,3]:
            get_answers = db.query(Option).filter(Option.question_id == question_id,Option.answer_status == 1).all()
            get_answer_ids = [option.id for option in get_answers]
            if sorted(answer_id) == sorted(get_answer_ids):
                  scored_mark = get_question_mark
      print(question_id,assigned_id)

      check_question_attened = db.query(StudentExamDetail).filter(StudentExamDetail.question_id==question_id,StudentExamDetail.assign_exam_id == assigned_id,StudentExamDetail.status ==1).first()
      print(check_question_attened)
      if check_question_attened:
            if type_id == 2:
                  check_question_attened.answer = answer
                  check_question_attened.mark = scored_mark
                  check_question_attened.updated_at = datetime.now(tz=settings.tz_IN)
            elif type_id in [1,3]:
                  check_question_attened.mark = scored_mark
                  check_question_attened.updated_at = datetime.now(tz=settings.tz_IN)
                  check_question_attened.option_ids = option
            elif type_id == 4:
                  check_question_attened.answer = answer
                  check_question_attened.updated_at = datetime.now(tz=settings.tz_IN)
      else:
            add_new = StudentExamDetail(
                        question_id=question_id,
                        option_ids = option,
                        answer=answer,
                        type__id=type_id,
                        student_id=user.id,
                        assign_exam_id=assigned_id,
                        status=1,
                        created_at=datetime.now(),
                        mark=scored_mark
                        )
            db.add(add_new)
      db.commit()
      return {"status":1,"msg":"Success"}


      # # get_total = db.query(func.sum(StudentExamDetail.mark)).group_by(StudentExamDetail.assign_exam_id).scalar()
      # # print(get_total,"score")
      # return {"status":1,"msg":"Success"}

@router.post("/view_answer")
async def viewAnswer(
                        db: Session = Depends(get_db),
                        token: str = Form(...),
                        question_id: int = Form(...),
                        assigned_id: int = Form(...)
):
      user=get_user_token(db=db,token=token)
      if not user:
         return {"status":0,"msg":"Your login session expires.Please login again."}
      get_question = db.query(Question).filter(Question.id == question_id, Question.status == 1).first()
      if not get_question:
            return {"status":0,"msg":"Question not found"}
      get_assigned = db.query(AssignExam).filter(AssignExam.id == assigned_id,AssignExam.status==1).first()
      if not get_assigned:
            return {"status":0,"msg":"Invaild details"}
      get_answer = db.query(StudentExamDetail).filter(StudentExamDetail.assign_exam_id == assigned_id,StudentExamDetail.question_id).first()
      if not get_answer:
            return {"status":0, "msg": "Please asnwer the question"}
      return {"status":1, "msg":"Success","data":{
            "question_id": get_answer.question_id,
            "answer_ids": [ data for data in get_answer.option_ids.split(",")] if get_answer.option_ids else None,
            "answer": get_answer.answer if get_answer.answer else None,
            "student_exam_id": get_answer.id
      }}

@router.post("/submit_answer")
async def submitAnswer(
                        db: Session = Depends(get_db),
                        assigned_id: int = Form(...),
                        token: str = Form(...)
):
      user=get_user_token(db=db,token=token)
      if not user:
         return {"status":0,"msg":"Your login session expires.Please login again."}
      
      get_assigned_details = db.query(AssignExam).filter(AssignExam.id == assigned_id, AssignExam.status == 1).first()
      if not get_assigned_details:
            return {"status":0, "msg":"Invaild details"}
      get_question_count = db.query(func.count(Question.id)).filter(Question.set_id == get_assigned_details.set_id,Question.status == 1).scalar()
      get_student_attended = db.query(func.count(StudentExamDetail.id)).filter(StudentExamDetail.assign_exam_id==assigned_id,StudentExamDetail.status ==1).scalar()
      if get_question_count != get_student_attended:
            return {"status":0, "msg": "Please answer all Question"}
      return {"status":1, "msg":"Exam successfully completed"}

@router.post("/attended_questions")
async def attendedQuestion(
                              db: Session = Depends(get_db),
                              assigned_id: int = Form(...),
                              token: str = Form(...)
):
      user=get_user_token(db=db,token=token)
      if not user:
         return {"status":0,"msg":"Your login session expires.Please login again."}
      # get_assigned_details = db.query(AssignExam).
      get_answered_questions = db.query(StudentExamDetail).filter(StudentExamDetail.assign_exam_id==assigned_id).all()
      get_answered_questions_ids = [ data.question_id for data in get_answered_questions]
      return {"status":1, "msg":"Success","data":get_answered_questions_ids}
      

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

@router.post("/exam_running_status")
async def examrunningStatus(
                              db: Session = Depends(get_db),
                              token: str = Form(...),
                              assigned_id: int = Form(...)
):
      user=get_user_token(db=db,token=token)
      if not user:
         return {"status":0,"msg":"Your login session expires.Please login again."}
      get_assigned_details = db.query(AssignExam).filter(AssignExam.status == 1, AssignExam.id == assigned_id)
      if not get_assigned_details:
            return {"status":0, "msg":"Invaild details"}
      if user.user_type == 3:
            # get_assigned_details = get_assigned_details.filter(AssignExam.student_id == user.id)
            exam_details = db.query(StudentExamDetail).filter(StudentExamDetail.assign_exam_id==assigned_id).first()
            # get_assigned_details = get_assigned_details.outerjoin(
            #       StudentExamDetail, StudentExamDetail.assign_exam_id == AssignExam.id
            #       ).filter(
            #       AssignExam.student_id == user.id,
            #       StudentExamDetail.assign_exam_id == None
            #       )

      if not exam_details:
            return {"status":1, "msg":"Running" ,"data":1}
      if exam_details:
            return {"status":1, "msg":"completed" ,"data":2}
      

      
