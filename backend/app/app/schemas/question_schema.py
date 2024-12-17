from pydantic import BaseModel
from typing import List, Optional
class Question(BaseModel):
    question_id:int
    type_id: int
    answer_id: list[int] | None = None
    answer:  Optional[str] = None

class GetAnswer(BaseModel):
    question_information:list[Question]
    assign_exam_id:int 
    token:str
 