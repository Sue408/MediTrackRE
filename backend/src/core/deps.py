"""
fast API依赖注入模块
- get_user: 验证用户请求中的token并解析返回用户ID
- get_db: 获取数据库会话
"""
from typing import Any, AsyncGenerator
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..db import session_factory
from .security import JWTManager

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

# ========= 用户token验证 =========
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
async def get_user_id(token: str=Depends(oauth2_scheme)) -> int:
    """
    检查用户token并返回用户ID

    Args:
        token: JWT token

    Returns:
        int: 用户ID
    """
    # 验证token并返回TokenData对象
    token_data = JWTManager.verify_token(token)

    return token_data.user_id

