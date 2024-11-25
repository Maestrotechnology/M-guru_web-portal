from fastapi import APIRouter

router = APIRouter()

@router.post("/home")
async def home():
    return "hello"