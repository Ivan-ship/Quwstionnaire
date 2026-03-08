import jwt
import os
from dotenv import load_dotenv
import datetime

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORIGHTM = "HS256"

#генерация токена
def generate_access_token(user_id: int, username: str, expires_time: int = 30):

    #Используем регианальное время(UTC)
    now = datetime.datetime.now(datetime.timezone.utc)
    expires_time = now + datetime.timedelta(minutes=expires_time)
    payload = {
        "user_id": user_id,
        "username": username,
        "iat": now,
        "exp": expires_time.timestamp()
    }

    token = jwt.encode(payload, SECRET_KEY, ALGORIGHTM)
    return token


#Декодирование токена
def decode_token(token: str) -> dict:
    try:
        payload(token, SECRET_KEY, algorihtm = [ALGORIGHTM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Время действия токена истекло!")
    except jwt.InvalidTokenError:
        raise Exception("Невалидный токен!")