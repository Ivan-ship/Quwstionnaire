from pydantic import BaseModel
from typing import List

class CreateTest(BaseModel):
    title: str
    user_id: int

class CreateAnswer(BaseModel):
    text: str

class CreateQuestion(BaseModel):
    text: str
    test_id: int
    answers: List[CreateAnswer]