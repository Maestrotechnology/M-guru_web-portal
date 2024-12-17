from pydantic import BaseModel

class Question(BaseModel):
    question_id: int
    type_id: int
    answer_id: list[int] | None = None
    answer: str | None = None

class GetAnswer(BaseModel):
    question_information: list[Question]
    token: str

class AddQuestion(BaseModel):
    question_title: str
    question_type_id: int
    mark: int
    exam_id: int
    set_id: int
    options: list[str] | None = None
    answer: list[str] | None = None

class GetQuestions(BaseModel):
    token: str 
    questions: list[AddQuestion]  
    
