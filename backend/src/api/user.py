"""
用户功能模块
"""
from fastapi import APIRouter
from pydantic import BaseModel

# ========= 初始化路由对象 ======
router = APIRouter()

# ========= 请求/响应模型定义 =========
# 1. 请求模型

# 2. 响应模型
class User(BaseModel):
    nickname: str
    email: str
    avatar: str

# ======== 路由端点定义 ========

