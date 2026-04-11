from routers.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Test(Base):
    
    __tablename__ = "tests"
    
    test_id = Column(Integer, primary_key=True, index = True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    
    questions = relationship("Question", back_populates = "test")

class Question(Base):
    
    __tablename__ = "questions"
    
    question_id = Column(Integer, primary_key=True, index = True, autoincrement=True)
    text = Column(String)
    test_id = Column(Integer, ForeignKey("tests.test_id"))
    
    answers = relationship("Answer", back_populates="question")
    
    

class Answer(Base):
    
    __tablename = "answers"
    
    answer_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text = Column(String)
    question_id = Column(Integer, ForeignKey("questions.question_id"))
    
    question = relationship("Question", back_populates="answer")