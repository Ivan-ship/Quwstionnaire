from fastapi import APIRouter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

router = APIRouter()

@router.post("/createdTest")
def crete_test():
    return {"success": True}