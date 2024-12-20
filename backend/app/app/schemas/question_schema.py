from pydantic import BaseModel
from typing import List, Optional
class QuestionDetail(BaseModel):
    option_id: int
    answer_name: str
    answer_status:int

class GetAnswer(BaseModel):
    
    question_id:int 
    question_title:Optional[str] = None
    mark:Optional[int] = None
    question_information:Optional[list[QuestionDetail]] = None
    question_status:int
    fill_answer:Optional[str] = None
    token:str
 
