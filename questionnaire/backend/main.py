from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel, EmailStr
from app_auth.database import database
from fastapi import HTTPException
from app_auth.security import hash_password, verify_password

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
    

    #Хеширование пароля
    hashed_password = hash_password(user.password)
    
    database.users.insert_one({
        "email": user.email,
        "password": hashed_password
    })
    
    return {"message": "Вы успешно зарегистрировались"}

#POST запрос входа
@app.post("/login")
def login(user: User):
    db_user = database.users.find_one({"email": user.email})

    if not db_user:
        raise HTTPException(status_code=400, detail="Вы ещё не зарегистрировались!")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Не верный логин или парль!")
    
    return{"message": "Добро пожаловать!"}

#Подключение базы данных
@app.get("/connect-db")
def connect_db():
    collection = database.list_collection_names()
    return{"collection": collection}