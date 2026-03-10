"""
用户计划表模型定义
- id: 主键
- user_id: 关联用户外键
- name: 计划名称
- plan_type: 计划类型 (长期/周期)
- start_date: 开始时间
- end_date: 结束时间
- frequency_type: 用药频率类型
- frequency_detail: 用药频率详情
- time_points: 每日用药时间点
- sms_enabled: 是否启用短信提醒
- status: 计划状态
- created_at: 创建时间
- updated_at: 更新时间
"""
from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base


class Plan(Base):
    """用户计划表模型"""
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    plan_type: Mapped[str] = mapped_column(String(20), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    frequency_type: Mapped[str] = mapped_column(String(20), nullable=False)
    frequency_detail: Mapped[dict] = mapped_column(JSON, nullable=True)
    time_points: Mapped[list] = mapped_column(JSON, nullable=False)
    sms_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")
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
    user = relationship("User", back_populates="plans")
    tracks = relationship("Track", back_populates="plan")
    plan_drugs = relationship("PlanDrug", back_populates="plan")