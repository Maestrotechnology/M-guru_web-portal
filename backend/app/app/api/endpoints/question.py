from fastapi import APIRouter,Form,Depends
from app.utils import *
from app.api.deps import *
import json
from sqlalchemy import func


router = APIRouter()

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
        print(options)
        print(answers)
        get_exam = db.query(Exam).filter(Exam.status==1,Exam.id==exam_id).first()
        if not get_exam:
            return {"status":0, "msg":"Invaild exam"}
        get_question_type = db.query(TypeOfQuestion).filter(TypeOfQuestion.id == question_type_id,TypeOfQuestion.status==1).first()
        if not get_question_type:
            return {"status":0, "msg":"Invaild question type"}
        get_set = db.query(Set).filter(Set.id == set_id, Set.exam_id == exam_id, Set.status == 1).first()
        if not get_set:
            return {"status":0, "msg":"Invaild set and exam"}
        
        if question_type_id in [1,3] and not options and not answers:
             return {"status":0, "msg":"Choose need options and answer"}
        
        create_question = Question(
            question_title = question_title,
            mark = mark,
            question_type_id = question_type_id,
            set_id = set_id,
            exam_id = exam_id,
            status = 1,
            no_of_answers = 1,
            created_at = datetime.now(settings.tz_IN),
            updated_at = datetime.now(settings.tz_IN)
        )
        db.add(create_question)
        db.commit()
        if options:
            if not answers:
                 return{"status":0, "msg":"You entered option but not entered answer"}
            # get_options = options.split(",")
            get_options = json.loads(options)
            print(get_options)
            for option in get_options:
                create_option = Option(
                    name = option,
                    answer_status = 2,
                    question_id = create_question.id,
                    status = 1,
                    created_at = datetime.now(settings.tz_IN),
                    updated_at = datetime.now(settings.tz_IN)
                )
                print(option)
                db.add(create_option)
                db.commit()
        if answers:
            # get_answers = answers.split(",")
            if question_type_id!=2:
                get_answers = json.loads(answers)
                print(get_answers)
            if question_type_id == 1:
                    print(get_answers.get("name"))
                    create_option = Option(
                            name = get_answers.get("name"),
                            answer_status = 1,
                            question_id = create_question.id,
                            status = 1,
                            created_at = datetime.now(settings.tz_IN),
                            updated_at = datetime.now(settings.tz_IN)
                        )
                    db.add(create_option)
            if question_type_id == 2:
                    create_option = Option(
                            name = answers,
                            answer_status = 1,
                            question_id = create_question.id,
                            status = 1,
                            created_at = datetime.now(settings.tz_IN),
                            updated_at = datetime.now(settings.tz_IN)
                        )
                    db.add(create_option)
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
                        page: int = 1,
                        size: int = 50

):
        user = get_user_token(db=db,token=token)
        if not user:
            return {"status":0,"msg":"Your login session expires.Please login again."}
        # if user.user_type not in [1,2]:
        #       return {"status":0, "msg":"Access denied"}
        
        get_set = db.query(Set).filter(Set.id == set_id,Set.status == 1,Set.exam_id == exam_id).first()
        if not get_set:
             return {"status": 0, "msg":"This Set of paper is Not found"}
        get_questions = db.query(Question).filter(
             Question.status==1,Question.set_id == set_id, Question.exam_id == exam_id
             )
        totalMarkForParticularPaper = db.query(func.sum(Question.mark)).filter(
             Question.status==1,Question.set_id == set_id, Question.exam_id == exam_id
             ).group_by(Question.set_id).scalar()
        print(totalMarkForParticularPaper)
        if question_id:
             get_questions = get_questions.filter(Question.id == question_id)
        if question_title:
             get_questions = get_questions.filter(Question.question_title.ilike(f"%{question_title}%"))
        if type_id:
             get_questions = get_questions.filter(Question.question_type_id == type_id)
        
        
        get_questions = get_questions.order_by(Question.id)
        totalCount= get_questions.count()
        total_page,offset,limit=get_pagination(totalCount,page,size)
        get_questions=get_questions.limit(limit).offset(offset).all()

        dataList =[]
    
        for question in get_questions:
                get_option = []
                get_answer = []
                if question.options:
                     for option in question.options:
                          if option.status ==1:# and option.answer_status	!=1:
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
                    "mark": question.mark,
                    "type_id": question.question_type_id,
                    "type": question.type_of.name,
                    "set_id": question.set_id,
                    "exam_id": question.exam_id
                
                })
        data=({"page":page,"size":size,"total_page":total_page,
                    "total_count":totalCount,"total_mark":totalMarkForParticularPaper,
                    "items":dataList,})
        return {"status":1,"msg":"Success","data":data}

@router.post("/update_question")
async def updateQuestion(
                            db: Session = Depends(get_db),
                            token: str = Form(...),
                            question_id: int = Form(...),
                            question_title: str = Form(...),
                            options: str = Form(None, description="option1,option2,option3"),
                            answers: str = Form(None, description="answer1,answer2,answer3"),
):
        get_question = db.query(Question).filter(Question.id == question_id, Question.status == 1).first()
        if not get_question:
             return {"status":0, "msg": "Question not found"}
        get_question.question_title = question_title
        if options:
            get_options = options.split(",")
            for option in get_options:
                 create_option = Option(
                    name = option,
                    answer_status = 2,
                    question_id = question_id,
                    status = 1,
                    created_at = datetime.now(settings.tz_IN),
                    updated_at = datetime.now(settings.tz_IN)
                )
                 db.add(create_option)
            db.commit()
        if answers:
            get_answers = answers.split(",")
            for option in get_answers:
                 create_option = Option(
                    name = option,
                    answer_status = 1,
                    question_id = question_id,
                    status = 1,
                    created_at = datetime.now(settings.tz_IN),
                    updated_at = datetime.now(settings.tz_IN)
                )
                 db.add(create_option)
            db.commit()
        return {"status":1, "msg":"Question updated Successfully"}

@router.post("/delete_option_and_answer")
async def deleteOptionAndAnswer(
                                    db: Session = Depends(get_db),
                                    token: str = Form(...),
                                    id: int = Form(...)
): 
        get_option = db.query(Option).filter(Option.id == id , Option.status == 1).first()
        if not get_option:
             return {"status": 0, "msg":"Option not found"}
        get_option.status = -1
        db.commit()
        return {"status":1, "msg":"Deleted successfully"}



        