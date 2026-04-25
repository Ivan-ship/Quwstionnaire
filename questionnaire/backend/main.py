from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from routers import auth, pages
from routers.dependencies import get_db
from routers.database import engine, Base
from models import user_models
from routers.redis_db import r
import redis
from datetime import datetime
import asyncio
from sqlalchemy import text
from utils.cleanup import clean_pending_users, clean_reset_password
from logic import create, take_test
import uvicorn
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


app = FastAPI()

app.mount(
    "/frontend",
    StaticFiles(directory=str(FRONTEND_DIR)),
    name="frontend"
)

app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(create.router)
app.include_router(take_test.router)


@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind = engine)
    asyncio.create_task(clean_up())


async def clean_up():
    while True:
        try:
            print("cleanup running")
            clean_pending_users()
            clean_reset_password()
        except Exception as e:
            print("cleanup error:", e)

        await asyncio.sleep(60)

@app.get("/connect-redis")
def connect_redis():
    try:
        r.ping()
        return{"status": "connected"}
    except Exception as ex:
         return {"status": "error", "message": str(ex)}


# Подключение postgresql
@app.get("/connect-postgresql")
def connect_postgres():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT version();"))
            return{"status": "connected"}
    except Exception as ex:
        return {"status": "error", "message": str(ex)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=124)