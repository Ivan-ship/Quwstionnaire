from routers.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Test(Base):

    __tablename__ = "tests"

    test_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey("users.user_id"))

    user = relationship("User", back_populates="tests")
    questions = relationship("Question", back_populates="test")
    user_results = relationship("UserResult", back_populates="test")

class Question(Base):
    
    __tablename__ = "questions"
    
    question_id = Column(Integer, primary_key=True, index = True, autoincrement=True)
    text = Column(String)
    test_id = Column(Integer, ForeignKey("tests.test_id"))
    
    answers = relationship("Answer", back_populates="question")
    test = relationship("Test", back_populates="questions")
    user_answers = relationship("UserAnswer", back_populates="question")
    
    

class Answer(Base):
    
    __tablename__ = "answers"
    
    answer_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text = Column(String)
    question_id = Column(Integer, ForeignKey("questions.question_id"))
    
    question = relationship("Question", back_populates="answers")
    user_answers = relationship("UserAnswer", back_populates="answer")

class UserAnswer(Base):

    __tablename__ = "users_answer"

    user_answer_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    question_id = Column(Integer, ForeignKey("questions.question_id"))
    answer_id = Column(Integer, ForeignKey("answers.answer_id"))
    test_result_id = Column(Integer, ForeignKey("users_results.test_result_id"))
    
    user = relationship("User", back_populates="user_answers")
    question = relationship("Question", back_populates="user_answers")
    answer = relationship("Answer", back_populates="user_answers")
    test_result = relationship("UserResult", back_populates="answers")


class UserResult(Base):

    __tablename__ = "users_results"

    test_result_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    completed_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    test_id = Column(Integer, ForeignKey("tests.test_id"))

    user = relationship("User", back_populates="user_results")
    test = relationship("Test", back_populates="user_results")
    answers = relationship("UserAnswer", back_populates="test_result")