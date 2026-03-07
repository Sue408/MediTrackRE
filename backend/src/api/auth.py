"""
用户验证模块，包含注册、登录、token刷新接口
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from ..core import get_db, PasswordHasher, JWTManager, TokenData
from ..models import User
# ========= 初始化路由对象 =========
router = APIRouter()

# ========= 请求/响应模块定义 =========
# 1. 请求模型
class RegisterRequest(BaseModel):
    """注册请求模型"""
    nickname: str
    email: str
    password: str

class LoginRequest(BaseModel):
    """登录请求模型"""
    email: str
    password: str

class RefreshRequest(BaseModel):
    """token刷新请求模型"""
    refresh_token: str

# 2. 响应模型
class TokenResponse(BaseModel):
    """token响应模型"""
    access_token: str
    refresh_token: str
    token_type: str

class LoginResponse(BaseModel):
    """登录响应模型"""
    nickname: str
    email: str
    created_at: datetime
    token: TokenResponse # token响应模型

# ========= 路由端点定义 =========
@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"description": "邮箱已被注册"}
    }
)
async def register(
        request: RegisterRequest,
        db: Session = Depends(get_db)
):
    """
    用户注册接口

    - **nickname**: 用户昵称 (1-50字符)
    - **email**: 有效的邮箱地址
    - **password**: 密码 (至少6位)
    """
    # 检查注册邮箱是否已经被注册
    existing_user: User|None = db.query(User).filter(
        User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="邮箱已被注册"
        )

    # 创建新用户
    password_hash: str = PasswordHasher.get_hashed_password(request.password)
    user = User(
        nickname=request.nickname,
        email=request.email,
        password_hash=password_hash
    )
    db.add(user)
    db.commit()
    db.refresh(user)

@router.post(
    "/login",
    response_model=LoginResponse,
    responses={
        401: {"description": "登录失败"}
    }
)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    用户登录接口

    - **email**: 邮箱地址
    - **password**: 明文密码
    """
    # 查询对应用户
    user = db.query(User).filter(
        User.email == request.email).first()

    # 如果用户不存在则返回409错误
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )

    # 验证密码是否正确
    if not PasswordHasher.verify_password(request.password,
                                          user.password_hash): # noqa
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误"
        )

    # 生成新的token
    token_data: TokenData = TokenData(user_id=user.id, nickname=user.nickname) # noqa
    access_token: str = JWTManager.create_access_token(token_data)
    refresh_token: str = JWTManager.create_refresh_token(token_data)

    return LoginResponse(
        nickname=user.nickname, # noqa
        email=user.email, # noqa
        created_at=user.created_at, # noqa
        token=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer"
        )
    )

@router.post(
    "/refresh",
    response_model=TokenResponse,
    responses={
        401: {"description": "token解析失败，用户不存在"},
        403: {"description": "账户已被禁用，无法刷新token"}
    }
)
async def refresh(request: RefreshRequest, db: Session = Depends(get_db)):
    """
    token 刷新接口

    - **refresh_token**: 刷新token
    """
    # 验证刷新token
    token_data = JWTManager.verify_token(request.refresh_token)

    # 解析token内容
    if token_data.user_id is None or token_data.nickname is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token解析失败"
        )

    # 查询用户信息与状态
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在或被封禁"
        )

    # 生成新的access token
    access_token: str = JWTManager.create_access_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=request.refresh_token,
        token_type="Bearer"
    )
