from fastapi import HTTPException, Response, APIRouter, Cookie
from fastapi.responses import RedirectResponse
from models.user_models import User, RegisterUser, Confirm, LoginUser, ResetRequest, ResetConfirm, PendingUser, ResetPassword
from routers.redis_db import r
from utils.security import hash_password, verify_password
from utils.token_utils import (
    generate_access_token, 
    generate_refressh_token, 
    SECRET_KEY,
    ALGORIGHTM)
from utils.activation_code import generate_activation_code
from fastapi import Request
from utils.send_mail import send_email
from routers.database import SessionLocal
from datetime import datetime
from fastapi import Depends
from sqlalchemy.orm import Session
from routers.dependencies import get_db
from utils.config import (YANDEX_CLIENT_ID,
                          REDIRECT_URI, AUTHORIZE_URL, 
                          USERINFO_URL, ACCESS_TOKEN_URL, 
                          YANDEX_CLIENT_SECRET,
                          GITHUB_CLIENT_ID, GITHUB_REDIRECT_URL,
                          GITHUB_AUTHORIZE_URL,
                          GITHUB_SCOPE, GITHUB_CLIENT_SECRET, 
                          GITHUB_INFO, GITHUB_ACCESS_TOKEN_URL)
import httpx
import jwt
import redis
from utils.token_utils import decode_token
from passlib.exc import UnknownHashError

router = APIRouter()


@router.post("/register")
def register(user: RegisterUser, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Данный пользователь уже зарегистрирован!")
    
    activation_code = generate_activation_code()
    
    #Временный пользователь
    pending_user = PendingUser(
        email = user.email,
        password = hash_password(user.password),
        first_name = user.first_name,
        last_name = user.last_name,
        activation_code = activation_code,
        created_at = datetime.utcnow()
    )
    db.add(pending_user)
    db.commit()
    
    #Отправка кода
    send_email(user.email, activation_code)
    
    return {"message": "Код подтверждения отправлен!"}
    
    


#Регистрация через подтверждение кода
@router.post("/confirm")
def confirm(user: Confirm, response: Response, db: Session = Depends(get_db)):
    
    pending_user = db.query(PendingUser).filter(PendingUser.email == user.email).first()
    
    if not pending_user:
        raise HTTPException(status_code=400, detail="Пользователь не найден")
    
    
    if pending_user.activation_code != user.activation_code:
        raise HTTPException(status_code=400, detail="Введён не верный код")
    
      #Хеширование пароля
    hashed_password = pending_user.password
    
    new_user = User(
        email = pending_user.email,
        password = pending_user.password,
        first_name = pending_user.first_name,
        last_name = pending_user.last_name
    )

    db.add(new_user)
    db.delete(pending_user)
    db.commit()
    db.refresh(new_user)
    
    #Выдача токена после регистрации
    token = generate_access_token(user_id = str(new_user.user_id), username=pending_user.email.split("@")[0])
    
    #Сохранение токена в файл cookie
    response.set_cookie(
        key="access_token",
        value = token,
        httponly = True,
        max_age = 30 * 60,
        samesite = "lax"
    )

    return {"ok": True}

#POST запрос входа
@router.post("/login")
def login(user: LoginUser, response: Response, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Вы ещё не зарегистрировались!")
    
    if not db_user.password:
        raise HTTPException(status_code=400, detail="Вы зарегистрированы другим способом!")

    try:
        if not verify_password(user.password, db_user.password):
            raise HTTPException(status_code=400, detail="Не верный пароль!")
    except UnknownHashError:
        raise HTTPException(status_code=400, detail="Вы зарегистрированы другим способом!")
    
    

    # Генерация access токена
    access_token = generate_access_token(
        user_id = str(db_user.user_id), 
        username = db_user.email.split("@")[0], 
        remember_me = user.remember_me)
    
    # Генерация refresh токена
    refresh_token = generate_refressh_token(
        user_id = str(db_user.user_id), 
        username = db_user.email.split("@")[0])
    
    refresh_key = f"refresh:{str(db_user.user_id)}"
    
    result = r.set(refresh_key, refresh_token, ex = 60 * 60 * 24 * 30)
    print("refresh saved:", result) 
    
    #зАПОМНИТЬ ПОЛЬЗОВАТЕЛЯ 
    if user.remember_me:
        access_max_age = 60 * 60 * 24 * 30
    else:
        access_max_age = 30 * 60

    response.set_cookie("access_token", access_token, max_age = access_max_age, httponly = True)
    response.set_cookie("refresh_token", refresh_token, max_age = 60 * 60 * 24 * 30, httponly = True)

    return{
        "message": "Добро пожаловать!",
        "first_name": db_user.first_name,
        }


#Сброс пароля
@router.post("/reset")
def reset_password(user: ResetRequest, db: Session = Depends(get_db)):
    register_user = db.query(User).filter(User.email == user.email).first()
    
    if not register_user:
        raise HTTPException(status_code = 400, detail = "Пользователя не существует.")
    
    reset_code = generate_activation_code()
    
    #Верменная бд для хранения логина и кода активации
    reset_entry = ResetPassword(
        email = user.email,
        new_password = hash_password(user.new_password),
        code = reset_code,
        created_at = datetime.utcnow()
    )
    db.add(reset_entry)
    db.commit()

    send_email(user.email, reset_code)

    return{"message": "Код отправлен!"}


@router.post("/reset/confirm")
def confirm_reset_password(user: ResetConfirm, db: Session = Depends(get_db)):

    reset = db.query(ResetPassword).filter(ResetPassword.email == user.email).first()

    if not reset:
        raise HTTPException(status_code=400, detail="Запрос не найден!")

    if reset.code != user.activation_code:
        raise HTTPException(status_code=400, detail="Не верный код подтверждения!")
    
    db_user = db.query(User).filter(User.email == user.email).first()
    db_user.password = reset.new_password

    db.delete(reset)
    db.commit()
    
    return{"message": "Пароль успешно изменен!"}


#Обновление access_token
@router.post("/refresh")
def refresh_token(response: Response, refresh_token: str = Cookie(None)):
    if not refresh_token:
        raise HTTPException(status_code = 400, detail = "refresh_token не существует")
    

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms = [ALGORIGHTM])
        user_id = payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code = 401, detail = "Refresh истек")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail = "Не валидный токен!")
    
    stored_token = r.get(f"refresh:{user_id}")
    
    
    if not stored_token or stored_token.decode() != refresh_token:
        raise HTTPException(status_code = 400, detail = "Невалидный токен!")
    

    # Выдача нового токена
    new_access_token = generate_access_token(user_id, payload["username"])
    response.set_cookie(
        "access_token", 
        new_access_token, 
        max_age = 30 * 60, 
        httponly = True)

    return{"access_token": new_access_token}

#------------Yandex auth-----------------------

#Редирект на яндекс
@router.get("/auth/yandex/login")
def yandex_login():
    url = (
        f"{AUTHORIZE_URL}"
        f"?response_type=code"
        f"&client_id={YANDEX_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
    )
    return RedirectResponse(url)

@router.get("/auth/yandex/callback")
async def yandex_callback(code: str, response: Response, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:

        #Получение access токена
        token_resp = await client.post(
            ACCESS_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": YANDEX_CLIENT_ID,
                "client_secret": YANDEX_CLIENT_SECRET,                
            }
        )

        token_data = token_resp.json()
        access_token = token_data.get("access_token")

        if not access_token:
            raise HTTPException(status_code=400, detail="Не удалось получить токен!")

        #Пользователь
        user_resp = await client.get(
            USERINFO_URL,
            headers={"Authorization": f"OAuth {access_token}"}
        )

        user_data = user_resp.json()

    #Регистрациия/вход(пока по yandex id)
    yandex_id = user_data.get("id")
    email = user_data.get("default_email")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(
            email = email,
            password = "oauth",
            first_name = user_data.get("real_name", ""),
            last_name = ""
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
    token = generate_access_token(user_id = str(user.user_id), username = user.email.split("@")[0])
    
    resp = RedirectResponse("/hello")

    resp.set_cookie(
        key="access_token",
        value = token,
        httponly = True,
        max_age = 30 * 60,
        samesite = "lax"
    )

    return resp

#------------GitHub oath-----------------------
@router.get("/auth/github/login")
def github_auth():
    url = (
        f"{GITHUB_AUTHORIZE_URL}"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri={GITHUB_REDIRECT_URL}"
        f"&scope={GITHUB_SCOPE}"
    )
    return RedirectResponse(url)


@router.get("/auth/github/callback")
async def github_callback(code: str, response: Response, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        
        #access token
        
        token_resp = await client.post(
            GITHUB_ACCESS_TOKEN_URL,
            data = {
                "code": code,
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
            },
            headers={"Accept": "application/json"}
        )
        
        token_data = token_resp.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            raise HTTPException(status_code = 400, detail = "Токен не существет")
        
        user_resp = await client.get(
            GITHUB_INFO,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        user_data = user_resp.json()
    
    #Регистрация
    github_id = user_data["id"]
    email = user_data.get("email")
    
    if not email:
        emails_resp = await client.get(
        "https://api.github.com/user/emails",
            headers = {"Authorization": f"Bearer {access_token}"}
        )
        emails = emails_resp.json()
        #Подтвержденный email
        email = next((e["email"] for e in emails if e.get("verified")), None)

    user = db.query(User).filter(User.email == email).first()


    if not user:
        user = User(
            email = email,
            password = "oauth",
            first_name = user_data.get("name", ""),
            last_name = ""
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    token = generate_access_token(user_id=str(user.user_id), username = email.split("@")[0])

    resp = RedirectResponse("/hello")

    resp.set_cookie(
        key="access_token",
        value = token,
        httponly = True,
        max_age = 30 * 60,
        samesite = "lax"
    )
    
    return resp

#Данные пользователя после oauth
def get_current_user(
    access_token: str = Cookie(None), 
    db: Session = Depends(get_db)) -> User:
    if not access_token:
        raise HTTPException(status_code=400, detail="не залогинен")
    
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORIGHTM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Неверный токен")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Токен истёк")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Неверный токен")

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

# Выход(разлогинивание)
@router.post("/logout")
def logout(request: Request, response: Response):
    token = request.cookies.get("access_token")

    user_id = None
    
    #Добавляем токен в redis
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=  [ALGORIGHTM])
            user_id = str(payload.get("user_id"))
        except jwt.InvalidTokenError:
            user_id = None
            
        r.set(
            f"blacklist:{token}", "true",
            ex = 30 * 60)
        
       
        if user_id:
            delete = r.delete(f"refresh:{user_id}")
            print("refresh deleted:", delete)
        
    #Удаляем из cokkie
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    
    return {"message": "Успешный выход"}