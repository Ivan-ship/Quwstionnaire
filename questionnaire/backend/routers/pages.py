from fastapi.responses import FileResponse
from pathlib import Path
from fastapi import APIRouter

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

@router.get("/hello")
def hello():
    return FileResponse(FRONTEND_DIR / "hello.html")