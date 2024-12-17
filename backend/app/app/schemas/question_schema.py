from pydantic import BaseModel

class Question(BaseModel):
    question_id:int
    type_id: int
    answer_id: list[int] | None = None
    answer: str | None = None

class GetAnswer(BaseModel):
    question_information:list[Question]
    token:str
 