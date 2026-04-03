from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from routers import auth, pages
from routers.dependencies import get_db
from routers.redis_db import r
import redis
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

app = FastAPI()


app.mount("/frontend", StaticFiles(directory=str(FRONTEND_DIR)), name="frontend")

app.include_router(pages.router)
app.include_router(auth.router)


#Создание индексов при запуске
#@app.on_event("startup")
#def create_indexes():
    #database.pending_users.create_index("created_at", expireAfterSeconds = 300)
    #database.password_reset.create_index("created_at", expireAfterSeconds = 300)



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