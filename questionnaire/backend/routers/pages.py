from fastapi.responses import FileResponse
from pathlib import Path
from fastapi import APIRouter
from routers.auth import get_current_user
from fastapi import Depends
from models.user_models import User
from fastapi.responses import FileResponse, JSONResponse
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

def safe_file(name: str):
    file = FRONTEND_DIR / name
    if not file.exists():
        return JSONResponse(
            status_code = 404,
            content = {"error": f"{name} not found"}
        )
    return FileResponse(file)

router = APIRouter()

@router.get("/")
def root():
    return safe_file("index.html")


@router.get("/register")
def register_page():
    return safe_file("register.html")

@router.get("/reset")
def reset_page():
    return safe_file("reset.html")

@router.get("/email")
def confirm_email():
    return safe_file("email.html")

@router.get("/password")
def password_reset():
    return safe_file("password.html")

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
    return safe_file("hello.html")

@router.get("/test")
def test():
    return safe_file("test.html")

@router.get("/vote")
def take_vote():
    return safe_file("vote.html")