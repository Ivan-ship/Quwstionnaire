from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel, EmailStr
from auth.database import database
from fastapi import HTTPException

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

app = FastAPI()


app.mount("/frontend", StaticFiles(directory=str(FRONTEND_DIR)), name="frontend")

@app.get("/")
def root():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/register")
def register_page():
    return FileResponse(FRONTEND_DIR / "register.html")

class User(BaseModel):
    email: EmailStr
    password: str

@app.post("/register")
def register(user: User):
    existing_user = database.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Данный пользователь уже зарегистрирован!")
    
    database.users.insert_one({
        "email": user.email,
        "password": user.password
    })
    
    return {"message": "Вы успешно зарегистрировались"}

#Подключение базы данных
@app.get("/connect-db")
def connect_db():
    collection = database.list_collection_names()
    return{"collection": collection}