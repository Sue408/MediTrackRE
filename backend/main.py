"""
@File: main.py
@Author: Apnea
@project: Meditrack-Backend
Meditrack后端服务启动程序
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

# ========= 配置端口信息