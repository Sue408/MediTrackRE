"""
用户表模型定义
- id: 用户UID
- nickname: 用户昵称
- email: 注册邮箱
- avatar: 头像(Base64编码或图片URL)
- is_active: 是否激活
- created_at: 创建时间
- updated_at: 更新时间
"""
from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base

class User(Base):
    """用户表模型"""
    # 表名
    __tablename__ = "users"

    # UID
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # 昵称
    nickname: Mapped[str] = mapped_column(String(255), nullable=False)
    # 邮箱
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    # 密码hash
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    # 头像(Base64编码或图片URL)
    avatar: Mapped[str] = mapped_column(Text, nullable=True, default="")
    # 激活状态
    is_active: Mapped[bool] = mapped_column(Boolean, index=True, default=True)
    # 创建时间
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        index=True,
        nullable=False,
        default=datetime.now(timezone.utc)
    )
    # 更新时间
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        index=True,
        nullable=False,
        default=datetime.now(timezone.utc)
    )

    # 关联关系
    profile = relationship("Profile", back_populates="user", uselist=False)
    drugs = relationship("Drug", back_populates="user")
    plans = relationship("Plan", back_populates="user")
    tracks = relationship("Track", back_populates="user")
    relations = relationship("Relation", foreign_keys="Relation.user_id", back_populates="user")