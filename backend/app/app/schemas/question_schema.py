from typing import List, Optional
from pydantic import BaseModel


class QuestionDetail(BaseModel):
    option_id: Optional[int] = None
    answer_name: str
    answer_status:int
    is_new : int

class UpdateQuestion(BaseModel):
    
    question_id:int 
    question_title:Optional[str] = None
    mark:Optional[int] = None
    question_information:Optional[list[QuestionDetail]] = None
    type_of:int
    fill_answer:Optional[str] = None
    token:str


class GetQuestion(BaseModel):
    question_id: int
    type_id: int
    answer_id: list[int] | None = None
    answer:  Optional[str] = None

class GetAnswer(BaseModel):
    question_information:GetQuestion
    assign_exam_id:int 
    token:str
    # completed: int | None = None
    student_exam_id: int | None = None
 
