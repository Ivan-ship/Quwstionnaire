from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel, EmailStr
from app_auth.database import database
from fastapi import HTTPException
from app_auth.security import hash_password, verify_password
from app_auth.token_utils import generate_access_token
from fastapi import Response
from app_auth.activation_code import generate_activation_code

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

@app.get("/reset")
def reset_page():
    return FileResponse(FRONTEND_DIR / "reset.html")

class RegisterUser(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    
#Вход пользователя
class LoginUser(BaseModel):
    email: EmailStr
    password: str
    
    
class Confirm(BaseModel):
    email: EmailStr
    activation_code: str

@app.post("/register")
def register(user: RegisterUser, response: Response):
    existing_user = database.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Данный пользователь уже зарегистрирован!")
    
    activation_code = generate_activation_code()
    
    #Временный пользователь
    database.pending_users.insert_one({
        "email": user.email,
        "password": hash_password(user.password),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "activation_code": activation_code
    })
    
    return {"message": "Введите код активации"}



#Регистрация через подтверждение кода
@app.post("/confirm")
def confirm(user: Confirm, response: Response):
    
    pending_user = database.pending_users.find_one({"email": user.email})
    
    if not pending_user:
        raise HTTPException(status_code=400, detail="Пользователь не найден")
    
    
    if pending_user["activation_code"] != user.activation_code:
        raise HTTPException(status_code=400, detail="Введён не верный код")
    
      #Хеширование пароля
    hashed_password = pending_user["password"]
    
    database.users.insert_one({
        "email": pending_user["email"],
        "password": pending_user["password"],
        "first_name": pending_user["first_name"],
        "last_name": pending_user["last_name"]
    })
    
    database.pending_users.delete_one({"email": pending_user["email"]})
    
    #Выдача токена после регистрации
    token = generate_access_token(pending_user["email"], username=pending_user["email"].split("@")[0])
    

    #Сохранение токена в файл cookie
    response.set_cookie(
        key="access_token",
        value = token,
        httponly = True,
        max_age = 30 * 60,
        samesite = "lax"
    )

    return {"message": "Вы успешно зарегистрировались"}

#POST запрос входа
@app.post("/login")
def login(user: LoginUser, response: Response):
    db_user = database.users.find_one({"email": user.email})

    if not db_user:
        raise HTTPException(status_code=400, detail="Вы ещё не зарегистрировались!")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Не верный логин или парль!")
    

    #Выдача токена после регистрации
    token = generate_access_token(user.email, username = user.email.split("@")[0])
    
    #Сохранение токена в файл cookie
    response.set_cookie(
        key="access_token",
        value = token,
        httponly = True,
        max_age = 30 * 60,
        samesite = "lax"
    )

    return{"message": "Добро пожаловать!"}

#Подключение базы данных
@app.get("/connect-db")
def connect_db():
    collection = database.list_collection_names()
    return{"collection": collection}
