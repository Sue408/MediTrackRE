"""
@File: main.py
@Author: Apnea
@project: Meditrack-Backend
Meditrack后端服务启动程序
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core import config
from src.api import auth_router, user_router

# ========= 初始化数据库 =========
from src.db import Base, engine
import src.models # noqa
Base.metadata.create_all(bind=engine)

# ========= 实例化App对象并配置CORS =========
app = FastAPI(
    title="Meditrack-backend",
    description="Meditrack-backend API server",
    version="0.0.1",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ========= 注册子路由对象 =========
# 1. 根路由检测
@app.get("/")
async def root():
    """根路由端点函数"""
    return {"message": "connect success"}

# 2. Auth路由
app.include_router(
    auth_router,
    prefix="/api/auth",
    tags=["auth"]
    )

# 3. User路由
app.include_router(
    user_router,
    prefix="/api/user",
    tags=["user"]
    )

# 4. ...

# ========= 启动uvicorn服务 =========
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.host,
        port=config.port,
        reload=config.debug
    )