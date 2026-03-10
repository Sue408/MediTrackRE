"""
药品信息表模型定义
- id: 主键
- user_id: 关联用户外键
- name: 药品名称
- image: 药品图片
- usage_method: 用法
- dosage: 用量
- remaining: 余量
- source: 来源
- external_id: 外部数据库ID
- created_at: 创建时间
- updated_at: 更新时间
"""
from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base


class Drug(Base):
    """药品信息表模型"""
    __tablename__ = "drugs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    image: Mapped[str] = mapped_column(Text, nullable=True, default="")
    usage_method: Mapped[str] = mapped_column(String(50), nullable=False)
    dosage: Mapped[str] = mapped_column(String(50), nullable=False)
    remaining: Mapped[str] = mapped_column(String(50), nullable=True)
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    external_id: Mapped[int] = mapped_column(Integer, nullable=True)
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

    # 关联关系
    user = relationship("User", back_populates="drugs")
    plan_drugs = relationship("PlanDrug", back_populates="drug")