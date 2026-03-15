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
    # 表名
    __tablename__ = "drugs"

    # 主键
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # 外键: 关联用户UID
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    # 药品名称
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    # 药品图片(Base64编码或图片URL)
    image: Mapped[str] = mapped_column(Text, nullable=True, default="")
    # 用法
    usage_method: Mapped[str] = mapped_column(String(50), nullable=False)
    # 用量
    dosage: Mapped[str] = mapped_column(String(50), nullable=False)
    # 余量
    remaining: Mapped[str] = mapped_column(String(50), nullable=True)
    # 来源
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    # 外部数据库ID
    external_id: Mapped[int] = mapped_column(Integer, nullable=True)
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
    user = relationship("User", back_populates="drugs")
    plan_drugs = relationship("PlanDrug", back_populates="drug")