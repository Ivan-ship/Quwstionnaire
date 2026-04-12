from fastapi import APIRouter, Depends
from pathlib import Path
from sqlalchemy.orm import Session
from routers.dependencies import get_db
from schema.db_schema import CreateAnswer, CreateQuestion, CreateTest
from schema.pol_models import Question, Answer, Test
from routers.auth import get_current_user

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

router = APIRouter()

@router.post("/questions")
def crete_question(data: CreateQuestion, db: Session = Depends(get_db)):
    
    new_question = Question(
        text = data.text,
        test_id = data.test_id
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    
     
    for answ in data.answers:
        new_answer = Answer(
            text = answ.text,
            question_id = new_question.question_id
        )
        
        db.add(new_answer)
    db.commit()
    
    return {"message": "Question created"}

@router.post("/create_test")
def create_test(data: CreateTest, db:Session = Depends(get_db), user = Depends(get_current_user)):
    new_test = Test(
        title = data.title,
        user_id = user.user_id
    )
    db.add(new_test)
    db.commit()
    db.refresh(new_test)

    return{"test_id": new_test.test_id}