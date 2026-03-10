"""
用户关系映射表模型定义
- id: 主键
- user_id: 发起方用户外键
- target_user_id: 目标方用户外键
- relation_type: 关系类型 (患者/监护人)
- status: 关系状态
- remark: 备注名称
- created_at: 创建时间
- updated_at: 更新时间
"""
from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base


class Relation(Base):
    """用户关系映射表模型"""
    __tablename__ = "relations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    target_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    relation_type: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    remark: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc)
    )

    # 唯一约束: 同一对用户只能有一种关系
    __table_args__ = (
        UniqueConstraint('user_id', 'target_user_id', name='uq_user_target_relation'),
    )

    # 关联关系
    user = relationship("User", foreign_keys=[user_id], back_populates="relations")
    target_user = relationship("User", foreign_keys=[target_user_id])