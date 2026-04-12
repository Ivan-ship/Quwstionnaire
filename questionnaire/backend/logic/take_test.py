from fastapi import APIRouter, Depends, HTTPException
from pathlib import Path
from sqlalchemy.orm import Session
from routers.dependencies import get_db
from schema.pol_models import Test, UserAnswer, UserResult
from schema.db_schema import SubmitVote
from routers.auth import get_current_user

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

router = APIRouter()


@router.get("/tests")
def get_tests(db: Session = Depends(get_db)):
    tests = db.query(Test).all()
    return tests

@router.get("/tests/{test_id}")
def get_test(test_id: int, db: Session = Depends(get_db)):
    test = db.query(Test).filter(Test.test_id == test_id).first()

    if not test:
        raise HTTPException(status_code=404, detail="Опрос не найден")
    
    return test


#результат опроса
@router.post("/submit_vote")
def submit_vote(data: SubmitVote, db: Session = Depends(get_db), user = Depends(get_current_user)):
    result = UserResult(user_id = user.user_id, test_id = data.test_id)

    db.add(result)
    db.commit()

    #Ответы на вопросы
    for answ in data.answers:
        user_answer = UserAnswer(user_id = user.user_id, question_id = answ.question_id, answer_id = answ.answer_id)
        db.add(user_answer)
    db.commit()

    return {"message": "Головс принят"}