from pydantic import BaseModel
from typing import List

class CreateTest(BaseModel):
    title: str

class CreateAnswer(BaseModel):
    text: str

class CreateQuestion(BaseModel):
    text: str
    test_id: int
    answers: List[CreateAnswer]


class VoteItem(BaseModel):
    question_id: int
    answer_id: int

class SubmitVote(BaseModel):
    test_id: int
    answers: List[VoteItem]


class AnswerOut(BaseModel):
    answer_id: int
    text: str
    
    class Config:
        from_attributes = True


class QuestionOut(BaseModel):
    question_id: int
    text: str
    answer: List[AnswerOut]
    
    class Config:
        from_attributes = True


class TestOut(BaseModel):
    test_id: int
    title: str
    questions: List[QuestionOut]
    
    class Config:
        from_attributes = True