from fastapi import APIRouter,Form,Depends
from app.utils import *
from app.api.deps import *
import json
from sqlalchemy import func
from app.schemas import *
from fastapi.encoders import jsonable_encoder 
# import set 

router = APIRouter()

# @router.post("/add_question")
# async def addQuestions(
#                         db: Session = Depends(get_db),
#                         token: str = Form(...),
#                         question_type_id: int = Form(...,description="1->choose 2->fill in the blank 3->multi choise 4-> paragraph"),
#                         mark: int = Form(...),
#                         exam_id: int = Form(...),
#                         set_id: int = Form(...),
#                         question_title: str = Form(...),
#                         options: str = Form(None, description="option1,option2,option3"),
#                         answers: str = Form(None, description="answer1,answer2,answer3"),

# ):
#         user=get_user_token(db=db,token=token)
#         if not user:
#             return {"status":0,"msg":"Your login session expires.Please login again."}
#         if user.user_type not in [1,2]:
#              return {"status":0, "msg":"Access denied"}
#         get_exam = db.query(Exam).filter(Exam.status==1,Exam.id==exam_id).first()
#         if not get_exam:
#             return {"status":0, "msg":"Invaild exam"}
#         get_question_type = db.query(TypeOfQuestion).filter(TypeOfQuestion.id == question_type_id,TypeOfQuestion.status==1).first()
#         if not get_question_type:
#             return {"status":0, "msg":"Invaild question type"}
#         get_set = db.query(Set).filter(Set.id == set_id, Set.exam_id == exam_id, Set.status == 1).first()
#         if not get_set:
#             return {"status":0, "msg":"Invaild set and exam"}
        
#         if question_type_id in [1,3] and not options and not answers:
#              return {"status":0, "msg":"Choose need options and answer"}
#         create_question = Question(
#             question_title = question_title,
#             mark = mark,
#             question_type_id = question_type_id,
#             set_id = set_id,
#             exam_id = exam_id,
#             status = 1,
#             no_of_answers = 1,
#             created_at = datetime.now(settings.tz_IN),
#             updated_at = datetime.now(settings.tz_IN),
#             answer = answers if question_type_id == 2 else None
#         )
#         db.add(create_question)
#         db.commit()
#         if options:
#             if not answers:
#                  return{"status":0, "msg":"You entered option but not entered answer"}
#             get_options = options.split(",")
#             # get_options = json.loads(options)
#             for option in get_options:
#                 create_option = Option(
#                     name = option,
#                     answer_status = 2,
#                     question_id = create_question.id,
#                     status = 1,
#                     created_at = datetime.now(settings.tz_IN),
#                     updated_at = datetime.now(settings.tz_IN)
#                 )
#                 print(option)
#                 db.add(create_option)
#                 db.commit()
#         if answers:
#             if question_type_id!=2:
#                 get_answers = answers.split(",")
#                 # get_answers = json.loads(answers)
#                 print(get_answers)
#             if question_type_id == 1:
#                     print(get_answers.get("name"))
#                     create_option = Option(
#                             name = get_answers[0],
#                             answer_status = 1,
#                             question_id = create_question.id,
#                             status = 1,
#                             created_at = datetime.now(settings.tz_IN),
#                             updated_at = datetime.now(settings.tz_IN)
#                         )
#                     db.add(create_option)
#                     db.commit()
#             if question_type_id == 3:
#                     for answer in get_answers:
#                     # print(answer.get("name"))
#                         create_option = Option(
#                                 name = answer,
#                                 answer_status = 1,
#                                 question_id = create_question.id,
#                                 status = 1,
#                                 created_at = datetime.now(settings.tz_IN),
#                                 updated_at = datetime.now(settings.tz_IN)
#                             )
#                         db.add(create_option)
#                         db.commit()
#         return {"status":1, "msg":"Question add successfully"}




# @router.post("/update_question")
# async def update_question(*,
#                         db: Session = Depends(get_db),
#                         base: UpdateQuestion
# ):
#     # 
#     base=jsonable_encoder(base)
#     print(base)
#     question_id=base["question_id"]
#     question_title=base["question_title"]
#     mark=base["mark"]
#     type_of_question=base["type_of"]
#     fill_answer=base["fill_answer"]
#     if mark:
#         if not (0 < mark <= 100):
#             return {'status': 0, "msg": "Invalid mark"}
#     get_quesion=db.query(Question).filter(Question.id == question_id,Question.status ==1).first()
#     if not get_quesion:
#          return{"stauts":0, "msg":"Question not found"}
#     get_quesion.question_title = question_title
    
#     if type_of_question==2:
#         get_quesion.answer=fill_answer

#     if mark:
#         get_quesion.mark=mark
#     db.commit()

#     if type_of_question==1 or type_of_question ==3:#1->choose 3-> multi options
#         for data in base["question_information"]:
#             if data['is_new']==1:
#                 new_option = Option(
#                      name = data["answer_name"],
#                      answer_status = data["answer_status"] if data["answer_status"] else 2,
#                      status =1,
#                      created_at = datetime.now(settings.tz_IN),
#                      question_id = question_id,
#                 )
#                 db.add(new_option)
#                 db.commit()
#             elif data['is_new'] == 0:
#                 get_option=db.query(Option).filter(Option.id==data["option_id"],Option.status==1).first()
#                 if not get_option:
#                     return {"status":0, "msg":"Option not found"}
#                 get_option.name = data["answer_name"]
#                 get_option.answer_status = data["answer_status"] if data["answer_status"] else 2
#                 db.commit()
    
#     return ({"status":1,"msg":"Success."})

@router.post("/update_question")
async def update_question(*,
                        db: Session = Depends(get_db),
                        base: UpdateQuestion
):
    # 
    base=jsonable_encoder(base)
    token = base['token']
    user=get_user_token(db=db,token=token)
    if not user:
        return {"status":0,"msg":"Your login session expires.Please login again."}
    question_id=base["question_id"]
    question_title=base["question_title"]
    mark=base["mark"]
    type_of_question=base["type_of"]
    fill_answer=base["fill_answer"]
    if mark:
        if not (0 < mark <= 100):
            return {'status': 0, "msg": "Invalid mark"}
    get_question=db.query(Question).filter(Question.id == question_id,Question.status ==1).first()
    if not get_question:
         return{"stauts":0, "msg":"Question not found"}
    get_question.status=2
    db.commit()
    create_question = Question(
            question_title = question_title,
            mark = mark,
            question_type_id = type_of_question,
            set_id = get_question.set_id,
            exam_id = get_question.exam_id,
            status = 1,
            no_of_answers = 1,
            created_at = datetime.now(settings.tz_IN),
            created_by = user.id,
            updated_at = datetime.now(settings.tz_IN),
            answer = fill_answer if fill_answer else None
        )
    db.add(create_question)
    db.commit()

    if type_of_question==1 or type_of_question ==3:#1->choose 3-> multi options
        for data in base["question_information"]:
                new_option = Option(
                     name = data["answer_name"],
                     answer_status = data["answer_status"] if data["answer_status"] else 2,
                     status =1,
                     created_at = datetime.now(settings.tz_IN),
                     question_id = create_question.id,
                     created_by=user.id
                )
                db.add(new_option)
                db.commit()
    
    return ({"status":1,"msg":"Success."})

@router.post("/add_question")
async def addQuestions(
                        db: Session = Depends(get_db),
                        token: str = Form(...),
                        question_type_id: int = Form(...,description="1->choose 2->fill in the blank 3->multi choise 4-> paragraph"),
                        mark: int = Form(...),
                        exam_id: int = Form(...),
                        set_id: int = Form(...),
                        question_title: str = Form(...),
                        options: str = Form(None, description="option1,option2,option3"),
                        answers: str = Form(None, description="answer1,answer2,answer3"),
):
        user=get_user_token(db=db,token=token)
        if not user:
            return {"status":0,"msg":"Your login session expires.Please login again."}
        if user.user_type not in [1,2]:
             return {"status":0, "msg":"Access denied"}
        
        get_exam = db.query(Exam).filter(Exam.status==1,Exam.id==exam_id).first()
        if not get_exam:
            return {"status":0, "msg":"Invaild exam"}
        get_question_type = db.query(TypeOfQuestion).filter(TypeOfQuestion.id == question_type_id,TypeOfQuestion.status==1).first()
        if not get_question_type:
            return {"status":0, "msg":"Invaild question type"}
        get_set = db.query(QuestionSet).filter(QuestionSet.id == set_id, QuestionSet.exam_id == exam_id, QuestionSet.status == 1).first()
        if not get_set:
            return {"status":0, "msg":"Invaild set and exam"}
        if question_type_id in [1,3]: 
            count_options = len(json.loads(options))
            if type(json.loads(answers)) == list:
                count_answers = len(json.loads(answers))
            else:
                count_answers =1 if len(json.loads(answers)) ==2 else 0
            
            print(count_options,count_answers)
            # if not count_options and not count_answers:
            #     return {"status":0, "msg":"Choose need options and answer"}
            print(count_options + count_answers)
            if count_options + count_answers < 2:
                 return {"status":0,"msg":"Need atleast 2 options"}
            # if count_options + count_answers ==1  and question_type_id ==3:
            #      return {"status":0,"msg":"For multi choose need atleast 3 options"}
            
                 
                 
        create_question = Question(
            question_title = question_title,
            mark = mark,
            question_type_id = question_type_id,
            set_id = set_id,
            exam_id = exam_id,
            status = 1,
            no_of_answers = 1,
            created_at = datetime.now(settings.tz_IN),
            updated_at = datetime.now(settings.tz_IN),
            answer = answers if question_type_id == 2 else None
        )
        db.add(create_question)
        db.commit()
        if question_type_id in [1,3]:
            if options:
                if not answers:
                    return{"status":0, "msg":"You entered option but not entered answer"}
                # get_options = options.split(",")
                get_options = json.loads(options)
                for option in get_options:
                    create_option = Option(
                        name = option,
                        answer_status = 2,
                        question_id = create_question.id,
                        status = 1,
                        created_at = datetime.now(settings.tz_IN),
                        updated_at = datetime.now(settings.tz_IN)
                    )
                    db.add(create_option)
                    db.commit()
            if answers:
                # get_answers = answers.split(",")
                if question_type_id!=2:
                    get_answers = json.loads(answers)
                if question_type_id == 1:
                        create_option = Option(
                                name = get_answers.get("name"),
                                answer_status = 1,
                                question_id = create_question.id,
                                status = 1,
                                created_at = datetime.now(settings.tz_IN),
                                updated_at = datetime.now(settings.tz_IN)
                            )
                        db.add(create_option)
                        db.commit()
                # if question_type_id == 2:
                #         create_option = Option(
                #                 name = answers,
                #                 answer_status = 1,
                #                 question_id = create_question.id,
                #                 status = 1,
                #                 created_at = datetime.now(settings.tz_IN),
                #                 updated_at = datetime.now(settings.tz_IN)
                #             )
                #         db.add(create_option)
                if question_type_id == 3:
                        for answer in get_answers:
                        # print(answer.get("name"))
                            create_option = Option(
                                    name = answer.get("name"),
                                    answer_status = 1,
                                    question_id = create_question.id,
                                    status = 1,
                                    created_at = datetime.now(settings.tz_IN),
                                    updated_at = datetime.now(settings.tz_IN)
                                )
                            db.add(create_option)
                            db.commit()
                db.commit()
        return {"status":1, "msg":"Question add successfully"}

@router.post("/list_questions")
async def listQuestions(
                        db: Session = Depends(get_db),
                        token: str = Form(...),
                        set_id: int = Form(...),
                        exam_id: int = Form(...),
                        question_title: str = Form(None),
                        question_id: int = Form(None),
                        type_id: int = Form(None),
                        assigned_id: int = Form(None),
                        page: int = 1,
                        size: int = 50

):
        user = get_user_token(db=db,token=token)
        if not user:
            return {"status":0,"msg":"Your login session expires.Please login again."}
        # if user.user_type not in [1,2]:
        #       return {"status":0, "msg":"Access denied"}
        
        get_set = db.query(QuestionSet).filter(QuestionSet.id == set_id,QuestionSet.status == 1,QuestionSet.exam_id == exam_id).first()
        if not get_set:
             return {"status": 0, "msg":"This Set of paper is Not found"}
             
        get_questions = db.query(Question).filter(
             Question.status==1,Question.set_id == set_id, Question.exam_id == exam_id
             )
        totalMarkForParticularPaper = db.query(func.sum(Question.mark)).filter(
             Question.status==1,Question.set_id == set_id, Question.exam_id == exam_id
             ).group_by(Question.set_id).scalar()
        if question_id:
             get_questions = get_questions.filter(Question.id == question_id)
        if question_title:
             get_questions = get_questions.filter(Question.question_title.ilike(f"%{question_title}%"))
        if type_id:
             get_questions = get_questions.filter(Question.question_type_id == type_id)
        
        get_question_ids = []
        for question in get_questions:
             get_question_ids.append(question.id)
        get_questions = get_questions.order_by(Question.id.desc())
        totalCount= get_questions.count()
        total_page,offset,limit=get_pagination(totalCount,page,size)
        get_questions=get_questions.limit(limit).offset(offset).all()

        dataList =[]
        get_assigned = None
        get_student_answer = None
        response = {}
        #----------------------------
        if assigned_id:
            get_assigned = db.query(AssignExam).filter(AssignExam.id == assigned_id,AssignExam.status==1).first()
            if not get_assigned:
                return {"status":0,"msg":"Invaild details"}
            get_question_id = get_questions[0].id
            # if 
            get_student_answer = db.query(StudentExamDetail).filter(StudentExamDetail.assign_exam_id == assigned_id,StudentExamDetail.question_id == get_question_id).first()
            if get_student_answer:
                response["question_id"] = get_student_answer.question_id
                response["answer_ids"] = [ data for data in get_student_answer.option_ids.split(",")] if get_student_answer.option_ids else None
                response["answer"] = get_student_answer.answer if get_student_answer.answer else None,
                response["student_exam_id"] = get_student_answer.id
        #----------------------------
        for question in get_questions:
                get_option = []
                get_answer = []
                if question.options:
                     for option in question.options:
                          if user.user_type == 3:
                            if option.status ==1:# and option.answer_status	!=1:
                                get_option.append(
                                    {
                                    "option_id":option.id,
                                    "option":option.name
                                    }
                                    )
                          else:
                            if option.status ==1 and option.answer_status	!=1:
                                get_option.append(
                                    {
                                    "option_id":option.id,
                                    "option":option.name
                                    }
                                    )
                          if option.status == 1 and option.answer_status==1:
                               get_answer.append(
                                   {
                                   "option_id":option.id,
                                   "option":option.name
                                   }
                                   )
                dataList.append({
                    "question_id": question.id,
                    "question_title": question.question_title,
                    "options": get_option,
                    "answers": get_answer if user.user_type in [1,2] else None,
                    "fill_in_the_blank_answer": question.answer if question.answer and user.user_type in [1,2] else None,
                    "mark": question.mark,
                    "type_id": question.question_type_id,
                    "type": question.type_of.name,
                    "set_id": question.set_id,
                    "exam_id": question.exam_id,
                    "student_answer": response if assigned_id else None             
                })
        data=({"page":page,"size":size,"total_page":total_page,
                    "total_count":totalCount,"total_mark":totalMarkForParticularPaper,"question_ids": sorted(get_question_ids,reverse=True),
                    "items":dataList,})
        return {"status":1,"msg":"Success","data":data}

@router.post("/list_exam_questions")
async def listExamQuestions(
                        db: Session = Depends(get_db),
                        token: str = Form(...),
                        set_id: int = Form(...),
                        exam_id: int = Form(...),
                        question_title: str = Form(None),
                        question_id: int = Form(None),
                        type_id: int = Form(None),
                        assigned_id: int = Form(...),
                        page: int = 1,
                        size: int = 50

):
        user = get_user_token(db=db,token=token)
        if not user:
            return {"status":0,"msg":"Your login session expires.Please login again."}
        # if user.user_type not in [1,2]:
        #       return {"status":0, "msg":"Access denied"}
        
        get_set = db.query(QuestionSet).filter(QuestionSet.id == set_id,QuestionSet.status == 1,QuestionSet.exam_id == exam_id).first()
        if not get_set:
             return {"status": 0, "msg":"This Set of paper is Not found"}
        #get_assigned used to none but if used elsewhere check it
        get_assigned = db.query(AssignExam).filter(AssignExam.id == assigned_id,AssignExam.status==1).first()
        if not get_assigned:
                return {"status":0,"msg":"Invaild details"}
        get_assigned_questions = db.query(AssignedQuestion).filter(AssignedQuestion.status==1,AssignedQuestion.assign_exam_id==assigned_id).all()
        question_ids = []
        for assigned_question in get_assigned_questions:
             question_ids.append(assigned_question.question_id)
        get_questions = db.query(Question).filter(
             Question.id.in_(question_ids)
             )
        print(get_questions.count())
        totalMarkForParticularPaper = db.query(func.sum(Question.mark)).filter(
             Question.id.in_(question_ids)
             ).group_by(Question.set_id).scalar()
        if question_id:
             get_questions = get_questions.filter(Question.id == question_id)
        if question_title:
             get_questions = get_questions.filter(Question.question_title.ilike(f"%{question_title}%"))
        if type_id:
             get_questions = get_questions.filter(Question.question_type_id == type_id)
        
        get_question_ids = []
        for question in get_questions:
             get_question_ids.append(question.id)
        get_questions = get_questions.order_by(Question.id.desc())
        totalCount= get_questions.count()
        total_page,offset,limit=get_pagination(totalCount,page,size)
        get_questions=get_questions.limit(limit).offset(offset).all()

        dataList =[]
        get_assigned = None
        get_student_answer = None
        response = {}
        #----------------------------
        if assigned_id:
            get_assigned = db.query(AssignExam).filter(AssignExam.id == assigned_id,AssignExam.status==1).first()
            if not get_assigned:
                return {"status":0,"msg":"Invaild details"}
            get_question_id = get_questions[0].id
            # if 
            get_student_answer = db.query(StudentExamDetail).filter(StudentExamDetail.assign_exam_id == assigned_id,StudentExamDetail.question_id == get_question_id).first()
            if get_student_answer:
                response["question_id"] = get_student_answer.question_id
                response["answer_ids"] = [ data for data in get_student_answer.option_ids.split(",")] if get_student_answer.option_ids else None
                response["answer"] = get_student_answer.answer if get_student_answer.answer else None,
                response["student_exam_id"] = get_student_answer.id
        #----------------------------
        for question in get_questions:
                get_option = []
                get_answer = []
                if question.options:
                     for option in question.options:
                          if user.user_type == 3:
                            if option.status ==1:# and option.answer_status	!=1:
                                get_option.append(
                                    {
                                    "option_id":option.id,
                                    "option":option.name
                                    }
                                    )
                          else:
                            if option.status ==1 and option.answer_status	!=1:
                                get_option.append(
                                    {
                                    "option_id":option.id,
                                    "option":option.name
                                    }
                                    )
                          if option.status == 1 and option.answer_status==1:
                               get_answer.append(
                                   {
                                   "option_id":option.id,
                                   "option":option.name
                                   }
                                   )
                dataList.append({
                    "question_id": question.id,
                    "question_title": question.question_title,
                    "options": get_option,
                    "answers": get_answer if user.user_type in [1,2] else None,
                    "fill_in_the_blank_answer": question.answer if question.answer and user.user_type in [1,2] else None,
                    "mark": question.mark,
                    "type_id": question.question_type_id,
                    "type": question.type_of.name,
                    "set_id": question.set_id,
                    "exam_id": question.exam_id,
                    "student_answer": response if assigned_id else None             
                })
        data=({"page":page,"size":size,"total_page":total_page,
                    "total_count":totalCount,"total_mark":totalMarkForParticularPaper,"question_ids": sorted(get_question_ids,reverse=True),
                    "items":dataList,})
        return {"status":1,"msg":"Success","data":data}

@router.post("/delete_option_and_answer")
async def deleteOptionAndAnswer(
                                    db: Session = Depends(get_db),
                                    token: str = Form(...),
                                    id: int = Form(...)
):
        user=get_user_token(db=db,token=token)
        if not user:
            return {"status":0,"msg":"Your login session expires.Please login again."}
        if user.user_type not in [1,2]:
             return {"status":0, "msg":"Access denied"}
         
        get_option = db.query(Option).filter(Option.id == id , Option.status == 1).first()
        if not get_option:
             return {"status": 0, "msg":"Option not found"}
        get_option.status = -1
        db.commit()
        return {"status":1, "msg":"Deleted successfully"}

@router.post("/delete_question")
async def deleteQuestion(
                            db: Session = Depends(get_db),
                            token: str = Form(...),
                            question_id: int = Form(...)
):
        user=get_user_token(db=db,token=token)
        if not user:
            return {"status":0,"msg":"Your login session expires.Please login again."}
        if user.user_type not in [1,2]:
            return {"status":0, "msg":"Access denied"}
        
        get_question = db.query(Question).filter(Question.id == question_id, Question.status == 1).first()
        if not get_question:
            return {"status":0, "msg":"Question not found"}
        
        get_question.status = -1
        db.commit()
        return {"status":1, "msg":"question deleted successfully"}



        