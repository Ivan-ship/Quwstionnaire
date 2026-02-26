from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()


app.mount("/frontend", StaticFiles(directory="../frontend"), name="frontend")

@app.get("/")
def root():
    return FileResponse("../frontend/index.html")
