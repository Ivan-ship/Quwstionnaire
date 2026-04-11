from fastapi import APIRouter, Depends
from pathlib import Path
from sqlalchemy.orm import Session
from routers.dependencies import get_db
from schema.db_schema import CreateAnswer, CreateQuestion
from schema.pol_models import Question, Answer

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
            text = answ.tex,
            question_id = new_question.question_id
        )
        
        db.add(new_answer)
    db.commit()
    
    return {"message": "Question created"}