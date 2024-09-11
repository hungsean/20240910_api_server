from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/knock")
def knock():
    # 回傳一個 200 狀態的空訊息
    return JSONResponse(status_code=200, content={"message": "Knock received, everything's okay!"})
