"""
fast API依赖注入模块
- get_token_data: 验证用户请求中的token并解析得到token payload基础数据
- get_db: 获取数据库会话
"""
from typing import Any, AsyncGenerator
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..db import session_factory
from .security import JWTManager, TokenData

# ========= 用户token验证 =========
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
async def get_token_data(token: str=Depends(oauth2_scheme)) -> TokenData:
    """
    获取用户的token基础数据

    Args:
        token: JWT token

    Returns:
        TokenData: token中携带的基础数据
    """
    # 验证token并返回TokenData对象
    token_data = JWTManager.verify_token(token)
    return token_data

# ========= 获取数据库会话 =========
async def get_db() -> AsyncGenerator[Session, Any]:
    """
    获取数据库会话

    Returns:
        Session: 数据库会话对象
    """
    # 生成会话实例
    db: Session = session_factory()
    try:
        yield db
    finally:
        db.close()