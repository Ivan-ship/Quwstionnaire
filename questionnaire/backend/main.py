from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel, EmailStr

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

class User(BaseModel):
    email: EmailStr

@app.post("/register")
def register(user: User):
    return{'message': 'Регистрация прошла успешно!', 'email': user.email}