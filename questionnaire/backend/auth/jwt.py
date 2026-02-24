import jwt
import datetime
import secrets

#Создание ключа
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = 'HS256'

payload = {
    'user_id': 123,
    'username': 'ivanov_ivan',
    'iat': datetime.datetime.utcnow().timestamp(),
    'exp': (datetime.datetime.utcnow() + datetime.timedelta(minutes=15)).timestamp()
}

token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)