# from fastapi import FastAPI
# from fastapi import Request
# from fastapi.responses import JSONResponse
# from fastapi.responses import FileResponse
# from slowapi import Limiter
# from slowapi.util import get_remote_address
# from slowapi.middleware import SlowAPIMiddleware
# import os
# import random
# import sqlite3


# app = FastAPI()

# # 定義一個叫做 knock 的 API
# @app.get("/knock")
# def knock():
#     # 回傳一個 200 狀態的空訊息
#     return JSONResponse(status_code=200, content={"message": "Knock received, everything's okay!"})

# # 定義圖片資料夾路徑
# IMAGE_FOLDER = "asset\\images"


# limiter = Limiter(key_func=get_remote_address)
# app.state.limiter = limiter
# app.add_middleware(SlowAPIMiddleware)

# @app.get("/random-image")
# @limiter.limit("1/second")  
# def get_random_image(request: Request):
#     # 列出資料夾內所有圖片檔案
#     image_files = os.listdir(IMAGE_FOLDER)
    
#     # 隨機選擇一個圖片檔案
#     random_image = random.choice(image_files)
    
#     # 構造圖片的完整路徑
#     image_path = os.path.join(IMAGE_FOLDER, random_image)
    
#     # 回傳該圖片
#     return FileResponse(image_path)

# def get_random_image(input_class):
#     # 每次操作都建立一個新的連接
#     conn = sqlite3.connect('asset\\database\\image_info.db')
#     cursor = conn.cursor()

#     cursor.execute("SELECT filename FROM images WHERE class=? ORDER BY RANDOM() LIMIT 1", (input_class,))
#     result_image_filename = cursor.fetchone()

#     # 關閉連接
#     conn.close()

#     if result_image_filename:
#         return result_image_filename[0]
#     return None

# @app.get("/image/R0")
# @limiter.limit("1/second")  
# def get_random_r0(request: Request):
#     # cursor.execute("SELECT filename FROM images WHERE class='R0' ORDER BY RANDOM() LIMIT 1")
#     # result_image_filename = cursor.fetchone()
#     result_image_filename = get_random_image("R0")

#     # 構造圖片的完整路徑
#     image_path = os.path.join(IMAGE_FOLDER, result_image_filename)
    
#     # 回傳該圖片
#     return FileResponse(image_path)

# @app.get("/image/R15")
# @limiter.limit("1/second")  
# def get_random_r15(request: Request):
#     # cursor.execute("SELECT filename FROM images WHERE class='R0' ORDER BY RANDOM() LIMIT 1")
#     # result_image_filename = cursor.fetchone()
#     result_image_filename = get_random_image("R15")

#     # 構造圖片的完整路徑
#     image_path = os.path.join(IMAGE_FOLDER, result_image_filename)
    
#     # 回傳該圖片
#     return FileResponse(image_path)

# @app.get("/image/R18")
# @limiter.limit("1/second")  
# def get_random_r18(request: Request):
#     # cursor.execute("SELECT filename FROM images WHERE class='R0' ORDER BY RANDOM() LIMIT 1")
#     # result_image_filename = cursor.fetchone()
#     result_image_filename = get_random_image("R18")

#     # 構造圖片的完整路徑
#     image_path = os.path.join(IMAGE_FOLDER, result_image_filename)
    
#     # 回傳該圖片
#     return FileResponse(image_path)


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


from fastapi import FastAPI
from fastapi.responses import JSONResponse
from slowapi.middleware import SlowAPIMiddleware
from routers import knock, images
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager

# 創建限流器並使用基於IP的key
limiter = Limiter(key_func=get_remote_address)

# 定義 lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 在應用啟動時設置 limiter
    app.state.limiter = limiter
    yield
    # 應用關閉時的清理（如果需要）

app = FastAPI(lifespan=lifespan)
# app = FastAPI()

# 使用限流中介軟體
app.add_middleware(SlowAPIMiddleware)

# 定義全局限流異常處理器
@app.exception_handler(RateLimitExceeded)
async def ratelimit_handler(request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"message": "Rate limit exceeded"})


# 將 knock 的路由加入應用
app.include_router(knock.router)
# 將 images 的路由加入應用
app.include_router(images.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

