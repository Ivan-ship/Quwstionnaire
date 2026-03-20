import os
from dotenv import load_dotenv


YANDEX_CLIENT_ID = os.getenv("CLIENT_ID")
YANDEX_CLIENT_SECRET = os.getenv("CLIENT_SECRET")

AUTHORIZE_URL = "https://oauth.yandex.ru/authorize"
ACCESS_TOKEN_URL = "https://oauth.yandex.ru/token"
REDIRECT_URI = "http://127.0.0.1:8000/auth/yandex/callback"
USERINFO_URL = "https://login.yandex.ru/info"
