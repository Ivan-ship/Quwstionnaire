from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from routers import auth, pages

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

app = FastAPI()


app.mount("/frontend", StaticFiles(directory=str(FRONTEND_DIR)), name="frontend")

app.include_router(pages.router)
app.include_router(auth.router)

#Подключение базы данных
@app.get("/connect-db")
def connect_db():
    collection = database.list_collection_names()
    return{"collection": collection}
