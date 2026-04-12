from fastapi.responses import FileResponse
from pathlib import Path
from fastapi import APIRouter
from routers.auth import get_current_user
from fastapi import Depends
from models.user_models import User


BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

router = APIRouter()

@router.get("/")
def root():
    return FileResponse(FRONTEND_DIR / "index.html")


@router.get("/register")
def register_page():
    return FileResponse(FRONTEND_DIR / "register.html")

@router.get("/reset")
def reset_page():
    return FileResponse(FRONTEND_DIR / "reset.html")

@router.get("/email")
def confirm_email():
    return FileResponse(FRONTEND_DIR / "email.html")

@router.get("/password")
def password_reset():
    return FileResponse(FRONTEND_DIR / "password.html")

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "username": current_user.email.split("@")[0]
    }

@router.get("/hello")
def hello():
    return FileResponse(FRONTEND_DIR / "hello.html")

@router.get("/test")
def test():
    return FileResponse(FRONTEND_DIR / "test.html")

@router.get("/vote")
def take_vote():
    return FileResponse(FRONTEND_DIR / "vote.html")