"""
用户功能模块，包含获取和更新用户信息、密码和健康档案接口
"""
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..core import get_db, get_user_id, get_user_from_id, PasswordHasher
from ..models import User, Profile

# ========= 初始化路由对象 ======
router = APIRouter()

# ========= 请求/响应模型定义 =========
# 1. 请求模型
class UpdateUserInfoRequest(BaseModel):
    """更新用户信息请求模型"""
    nickname: str|None = None
    avatar: str|None = None

class AllergyItem(BaseModel):
    """过敏史项模型"""
    name: str
    reaction: str

class DiseaseItem(BaseModel):
    """疾病史项模型"""
    name: str
    diagnosed_at: Optional[str] = None
    status: str

class UpdateProfileRequest(BaseModel):
    """更新健康档案请求模型"""
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    blood_type: Optional[str] = None
    allergies: Optional[list[AllergyItem]] = None
    diseases: Optional[list[DiseaseItem]] = None
    special_status: Optional[str] = None

class ChangePasswordRequest(BaseModel):
    """修改密码请求模型"""
    old_password: str
    new_password: str
    confirm_password: str

# 2. 响应模型
class UserInfoResponse(BaseModel):
    """用户信息响应模型"""
    nickname: str
    email: str
    avatar: str
    created_at: datetime

class ProfileResponse(BaseModel):
    """健康档案响应模型"""
    id: int
    user_id: int
    gender: str
    height: Optional[float]
    weight: Optional[float]
    blood_type: str
    allergies: list[dict]
    diseases: list[dict]
    special_status: Optional[str]
    created_at: datetime
    updated_at: datetime

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
        user_id: int = Depends(get_user_id),
        db: Session = Depends(get_db)
    ):
    """
    获取当前用户信息接口

    通过token验证用户身份，返回用户信息
    """
    user = get_user_from_id(user_id=user_id, db=db)

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
            403: {"description": "账户已被禁用"},
            404: {"description": "用户不存在"}
        }
    )
async def update_user_info(
        request: UpdateUserInfoRequest,
        user_id: int = Depends(get_user_id),
        db: Session = Depends(get_db)
    ):
    """
    更新用户信息接口

    - **nickname**: 用户昵称（可选）
    - **avatar**: 头像，Base64编码或图片URL（可选）
    """
    # 获取用户对象
    user = get_user_from_id(user_id=user_id, db=db)

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

@router.get(
    "/profile",
    response_model=ProfileResponse,
    responses={
        401: {"description": "未登录或token无效"}
    }
)
async def get_profile(
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """
    获取健康档案接口
    """
    profile: Profile | None = db.query(Profile).filter(
        Profile.user_id == user_id
    ).first()

    if not profile:
        # 如果健康档案不存在，返回空档案
        profile = Profile(user_id=user_id)
        db.add(profile)
        db.commit()
        db.refresh(profile)

    # noinspection PyTypeChecker
    return ProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        gender=profile.gender,
        height=profile.height,
        weight=profile.weight,
        blood_type=profile.blood_type,
        allergies=profile.allergies,
        diseases=profile.diseases,
        special_status=profile.special_status,
        created_at=profile.created_at,
        updated_at=profile.updated_at
    )

@router.put(
    "/profile",
    response_model=ProfileResponse,
    responses={
        401: {"description": "未登录或token无效"}
    }
)
async def update_profile(
    request: UpdateProfileRequest,
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """
    更新健康档案接口

    - **gender**: 性别（男/女/unknown）
    - **height**: 身高（cm）
    - **weight**: 体重（kg）
    - **blood_type**: 血型（A/B/AB/O/unknown）
    - **allergies**: 过敏史数组
    - **diseases**: 疾病史数组
    - **special_status**: 女性特殊状态（备孕/怀孕/哺乳/null）
    """
    # 获取健康档案
    profile: Profile | None = db.query(Profile).filter(
        Profile.user_id == user_id
    ).first()

    # 如果不存在则创建
    if not profile:
        profile = Profile(
            user_id=user_id,
            gender="unknown",
            blood_type="unknown"
        )
        db.add(profile)
        db.flush()

    # 更新字段
    if request.gender is not None:
        profile.gender = request.gender
    if request.height is not None:
        profile.height = request.height
    if request.weight is not None:
        profile.weight = request.weight
    if request.blood_type is not None:
        profile.blood_type = request.blood_type
    if request.allergies is not None:
        profile.allergies = [item.model_dump() for item in request.allergies]
    if request.diseases is not None:
        profile.diseases = [item.model_dump() for item in request.diseases]
    if request.special_status is not None:
        profile.special_status = request.special_status

    profile.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(profile)

    # noinspection PyTypeChecker
    return ProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        gender=profile.gender,
        height=profile.height,
        weight=profile.weight,
        blood_type=profile.blood_type,
        allergies=profile.allergies,
        diseases=profile.diseases,
        special_status=profile.special_status,
        created_at=profile.created_at,
        updated_at=profile.updated_at
    )

@router.post(
    "/change-password",
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "未登录或token无效"},
        400: {"description": "密码错误或两次密码不一致"},
        403: {"description": "用户已经被禁用"},
        404: {"description": "用户不存在"}
    }
)
async def change_password(
    request: ChangePasswordRequest,
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """
    修改密码接口

    - **old_password**: 当前密码
    - **new_password**: 新密码（至少6位）
    - **confirm_password**: 确认新密码
    """
    # 查询用户
    user: User = get_user_from_id(user_id, db)

    # 验证旧密码
    if not PasswordHasher.verify_password(request.old_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="当前密码错误"
        )

    # 验证两次密码一致
    if request.new_password != request.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="两次输入的密码不一致"
        )

    # 验证新密码长度
    if len(request.new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="新密码长度至少6位"
        )

    # 更新密码
    user.password_hash = PasswordHasher.get_hashed_password(request.new_password)
    user.updated_at = datetime.now()
    db.commit()

    return {"message": "密码修改成功"}
