"""
API接口层
- auth_router: 验证与鉴权模块
- user_router: 用户模块
- drugs_router: 药品管理模块
- plans_router: 计划管理模块
"""
from .auth import router as auth_router
from .user import router as user_router
from .drugs import router as drugs_router
from .plans import router as plans_router

__all__ = [
    "auth_router",
    "user_router",
    "drugs_router",
    "plans_router"
]