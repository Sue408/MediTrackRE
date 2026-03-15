"""
健康档案表模型定义
- id: 主键
- user_id: 关联用户外键
- gender: 性别
- height: 身高 (cm)
- weight: 体重 (kg)
- blood_type: 血型
- allergies: 过敏史 (JSON)
- diseases: 疾病史 (JSON)
- special_status: 女性特殊状态
- created_at: 创建时间
- updated_at: 更新时间
"""
from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime, JSON, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base


class Profile(Base):
    """健康档案表模型"""
    # 表名
    __tablename__ = "profiles"

    # 主键
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # 外键: 关联用户UID
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    # 性别
    gender: Mapped[str] = mapped_column(String(20), nullable=False, default="unknown")
    # 身高
    height: Mapped[float] = mapped_column(Numeric(5, 2), nullable=True)
    # 体重
    weight: Mapped[float] = mapped_column(Numeric(5, 2), nullable=True)
    # 血型
    blood_type: Mapped[str] = mapped_column(String(10), nullable=False, default="unknown")
    # 过敏史
    allergies: Mapped[list[dict]] = mapped_column(JSON, nullable=False, default=list)
    # 疾病史
    diseases: Mapped[list[dict]] = mapped_column(JSON, nullable=False, default=list)
    # 女性专属特殊状态
    special_status: Mapped[str] = mapped_column(String(20), nullable=True)
    # 创建时间
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc)
    )
    # 更新时间
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc)
    )

    # 关联关系
    user = relationship("User", back_populates="profile")
