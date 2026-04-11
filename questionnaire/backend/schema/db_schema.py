from pydantic import BaseModel
from typing import List

class CreateAnswer(BaseModel):
    text: str

class CreateQuestion(BaseModel):
    text: str
    test_id: int
    answers: List[CreateAnswer]