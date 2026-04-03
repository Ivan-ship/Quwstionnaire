from sqlalchemy.orm import Session
from routers.database import SessionLocal, Base, engine

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
