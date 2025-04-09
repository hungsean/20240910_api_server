import os
import random
import sqlite3
from fastapi import APIRouter, Request, Depends
from fastapi.responses import FileResponse, JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()

limiter = Limiter(key_func=get_remote_address)

IMAGE_FOLDER = "./assets/images"
IMAGE_DB = "./assets/database/image_info.db"

def get_random_image_from_class(input_class):
    """從資料庫中根據 class 隨機獲取圖片檔案名"""
    try:
        # 使用 URI 模式，並設定只讀模式防止自動創建資料庫
        conn = sqlite3.connect(f"file:{IMAGE_DB}?mode=ro", uri=True)
        cursor = conn.cursor()

        cursor.execute("SELECT filename FROM images WHERE class=? ORDER BY RANDOM() LIMIT 1", (input_class,))
        result_image_filename = cursor.fetchone()

    except sqlite3.OperationalError as e:
        # 如果資料庫不存在或者無法連線，將會觸發例外
        raise FileNotFoundError(f"Database not found: {IMAGE_DB}") from e

    finally:
        # 確保即使發生例外，也會關閉連線
        conn.close()

    if result_image_filename:
        return result_image_filename[0]
    return None

def retrieve_image_response(image_filename):
    """生成圖片的回應或 404"""
    if not image_filename:
        return JSONResponse(status_code=404, content={"message": "Image not found"})
    
    image_path = os.path.join(IMAGE_FOLDER, image_filename)
    
    if not os.path.exists(image_path):
        return JSONResponse(status_code=404, content={"message": "File does not exist on server"})

    return FileResponse(image_path)

@router.get("/random-image")
@limiter.limit("2/second")
async def get_random_image_api(request: Request):
    """從文件夾隨機選擇一張圖片，並進行限流"""

    image_files = os.listdir(IMAGE_FOLDER)
    if not image_files:
        return JSONResponse(status_code=404, content={"message": "No images found"})
    
    random_image = random.choice(image_files)
    return retrieve_image_response(random_image)

CLASS = ["R0", "R15", "R18"]

@router.get("/image/{class_name}")
@limiter.limit("2/second")
async def get_random_image_by_class(request: Request, class_name: str):
    """根據 class 隨機選擇圖片，並進行限流"""

    if class_name not in CLASS:
        return JSONResponse(status_code=404, content={"message": "No Class found"})
    
    image_filename = get_random_image_from_class(class_name)
    return retrieve_image_response(image_filename)
