import os
from dotenv import load_dotenv


YANDEX_CLIENT_ID = os.getenv("CLIENT_ID")
YANDEX_CLIENT_SECRET = os.getenv("CLIENT_SECRET")

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

AUTHORIZE_URL = "https://oauth.yandex.ru/authorize"
ACCESS_TOKEN_URL = "https://oauth.yandex.ru/token"
REDIRECT_URI = "http://127.0.0.1:8000/auth/yandex/callback"
USERINFO_URL = "https://login.yandex.ru/info"


GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_REDIRECT_URL = "http://localhost:3000/auth/github/callback"
GITHUB_INFO = "https://api.github.com/user"
GITHUB_SCOPE = "user"
