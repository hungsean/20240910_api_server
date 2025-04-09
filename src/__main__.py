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

