"""
用户功能模块，包含获取和更新用户信息接口
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..core import get_db, TokenData, get_token_data
from ..models import User

# ========= 初始化路由对象 ======
router = APIRouter()

# ========= 请求/响应模型定义 =========
# 1. 请求模型
class UpdateUserInfoRequest(BaseModel):
    """更新用户信息请求模型"""
    nickname: str | None = None
    avatar: str | None = None

# 2. 响应模型
class UserInfoResponse(BaseModel):
    """用户信息响应模型"""
    nickname: str
    email: str
    avatar: str
    created_at: datetime

# ======== 路由端点定义 ========
@router.get(
    "/info",
    response_model=UserInfoResponse,
    responses={
            401: {"description": "未登录或token无效"},
            403: {"description": "账户已被禁用"},
            404: {"description": "用户不存在"}
        }
    )
async def get_user_info(
        token_data: TokenData = Depends(get_token_data),
        db: Session = Depends(get_db)
    ):
    """
    获取当前用户信息接口

    通过token验证用户身份，返回用户信息
    """
    # 获取用户ID
    user_id: int = token_data.user_id

    # 查询用户是否存在
    user: User|None = db.query(User).filter(User.id == user_id).first() # noqa
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 查询用户状态
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用"
        )

    return UserInfoResponse(
        nickname=user.nickname,
        email=user.email,
        avatar=user.avatar,
        created_at=user.created_at
    )

@router.put(
    "/info",
    response_model=UserInfoResponse,
    responses={
            401: {"description": "未登录或token无效"},
            403: {"description": "账户已被禁用"}
        }
    )
async def update_user_info(
        request: UpdateUserInfoRequest,
        token_data: TokenData = Depends(get_token_data),
        db: Session = Depends(get_db)
    ):
    """
    更新用户信息接口

    - **nickname**: 用户昵称（可选）
    - **avatar**: 头像，Base64编码或图片URL（可选）
    """
    # 获取用户ID
    user_id: int = token_data.user_id

    # 查询用户是否存在
    user: User | None = db.query(User).filter(User.id == user_id).first()  # noqa
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 查询用户状态
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用"
        )

    # 更新昵称（如果提供）
    if request.nickname is not None:
        user.nickname = request.nickname

    # 更新头像（如果提供）
    if request.avatar is not None:
        user.avatar = request.avatar

    db.commit()
    db.refresh(user)

    return UserInfoResponse(
        nickname=user.nickname,
        email=user.email,
        avatar=user.avatar,
        created_at=user.created_at
    )
