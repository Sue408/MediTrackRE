"""
常用工具模块
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models import User

def get_user_from_id(user_id: int, db: Session) -> User:
    """
    根据用户ID获取用户数据库对象

    Args:
        user_id: 用户ID
        db: 数据库会话

    Returns:
        User: 用户数据库对象
    """
    user: User|None = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="用户不存在")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="用户已被禁用")

    return user