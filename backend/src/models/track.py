"""
历史用药记录表模型定义
- id: 主键
- user_id: 关联用户外键
- plan_id: 关联计划外键
- taken: 是否已服药
- taken_at: 实际服药时间
- created_at: 创建时间
"""
from datetime import datetime, timezone
from sqlalchemy import Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base


class Track(Base):
    """历史用药记录表模型"""
    __tablename__ = "tracks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    plan_id: Mapped[int] = mapped_column(Integer, ForeignKey("plans.id"), nullable=False, index=True)
    taken: Mapped[bool] = mapped_column(Boolean, default=False)
    taken_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc)
    )

    # 关联关系
    user: relationship = relationship("User", back_populates="tracks")
    plan: relationship = relationship("Plan", back_populates="tracks")