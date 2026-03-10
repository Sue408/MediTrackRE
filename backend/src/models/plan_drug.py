"""
计划药品中间表模型定义
- id: 主键
- plan_id: 关联计划外键
- drug_id: 关联药品外键
- dosage: 计划内的药品用量
"""
from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base


class PlanDrug(Base):
    """计划药品中间表模型"""
    __tablename__ = "plan_drugs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    plan_id: Mapped[int] = mapped_column(Integer, ForeignKey("plans.id"), nullable=False, index=True)
    drug_id: Mapped[int] = mapped_column(Integer, ForeignKey("drugs.id"), nullable=False, index=True)
    dosage: Mapped[str] = mapped_column(String(50), nullable=False)

    # 唯一约束: 同一计划中同一药品只能出现一次
    __table_args__ = (
        UniqueConstraint('plan_id', 'drug_id', name='uq_plan_drug'),
    )

    # 关联关系
    plan = relationship("Plan", back_populates="plan_drugs")
    drug = relationship("Drug", back_populates="plan_drugs")