from fastapi import HTTPException, Response, APIRouter
from models.user_models import RegisterUser, LoginUser, Confirm, ResetRequest, ResetConfirm
from utils.security import hash_password, verify_password
from utils.token_utils import generate_access_token
from utils.activation_code import generate_activation_code
from utils.send_mail import send_email
from routers.database import database

router = APIRouter()

@router.post("/register")
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

    #Отправка кода
    send_email(user.email, activation_code)


#Регистрация через подтверждение кода
@router.post("/confirm")
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
@router.post("/login")
def login(user: LoginUser, response: Response):
    db_user = database.users.find_one({"email": user.email})

    if not db_user:
        raise HTTPException(status_code=400, detail="Вы ещё не зарегистрировались!")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Не верный логин или парль!")
    

    #Выдача токена после регистрации
    token = generate_access_token(user.email, username = user.email.split("@")[0])
    
    #зАПОМНИТЬ ПОЛЬЗОВАТЕЛЯ 
    if user.remember_me:
        max_age = 60 * 60 * 24 * 30
    else:
        max_age = 30 * 60

    #Сохранение токена в файл cookie
    response.set_cookie(
        key="access_token",
        value = token,
        httponly = True,
        max_age = max_age,
        samesite = "lax"
    )

    return{"message": "Добро пожаловать!"}


#Сброс пароля
@router.post("/reset")
def reset_password(user: ResetRequest):
    register_user = database.users.find_one({"email": user.email})
    
    if not register_user:
        raise HTTPException(status_code = 400, detail = "Пользователя не существует.")
    
    reset_code = generate_activation_code()
    
    #Верменная бд для хранения логина и кода активации
    database.password_reset.insert_one({
        "email": user.email,
        "new_password": hash_password(user.new_password),
        "code": reset_code})
    send_email(user.email, reset_code)
    return{"message": "Код отправлен!"}


@router.post("/reset/confirm")
def confirm_reset_password(user: ResetConfirm):

    reset = database.password_reset.find_one({"email": user.email})

    if not reset:
        raise HTTPException(status_code=400, detail="Запрос не найден!")

    if reset["code"] != user.activation_code:
        raise HTTPException(status_code=400, detail="Не верный код подтверждения!")
    
    database.users.update_one({"email": user.email}, 
    {"$set":{"password": reset["new_password"]}})
    database.password_reset.delete_one({"email": user.email})
    
    return{"message": "Пароль успешно изменен!"}
