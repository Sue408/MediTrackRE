"""
计划管理模块，包含用药计划的CRUD和用药记录接口
"""
from datetime import datetime, date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from ..core import get_db, get_user_id
from ..models import Plan, PlanDrug, Drug, Track

# ========= 初始化路由对象 =========
router = APIRouter()

# ========= 请求/响应模型定义 =========
# 1. 请求模型
class PlanDrugRequest(BaseModel):
    """计划关联药品请求模型"""
    drug_id: int
    dosage: str

class CreatePlanRequest(BaseModel):
    """创建计划请求模型"""
    name: str
    plan_type: str
    start_date: datetime
    end_date: Optional[datetime] = None
    frequency_type: str
    frequency_detail: Optional[dict] = None
    time_points: list[str]
    sms_enabled: bool = False
    drug_ids: list[PlanDrugRequest]

class UpdatePlanRequest(BaseModel):
    """更新计划请求模型"""
    name: Optional[str] = None
    plan_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    frequency_type: Optional[str] = None
    frequency_detail: Optional[dict] = None
    time_points: Optional[list[str]] = None
    sms_enabled: Optional[bool] = None
    drug_ids: Optional[list[PlanDrugRequest]] = None

class TrackRequest(BaseModel):
    """记录用药请求模型"""
    time_point: str

# 2. 响应模型
class DrugBaseResponse(BaseModel):
    """药品基本信息响应模型"""
    id: int
    name: str
    usage_method: str
    image: Optional[str] = None

class PlanDrugResponse(BaseModel):
    """计划关联药品响应模型"""
    id: int
    plan_id: int
    drug_id: int
    dosage: str
    drug: DrugBaseResponse

class PlanResponse(BaseModel):
    """计划响应模型"""
    id: int
    user_id: int
    name: str
    plan_type: str
    start_date: datetime
    end_date: Optional[datetime]
    frequency_type: str
    frequency_detail: Optional[dict]
    time_points: list[str]
    sms_enabled: bool
    status: str
    created_at: datetime
    updated_at: datetime
    drugs: list[PlanDrugResponse]

class PaginatedPlansResponse(BaseModel):
    """分页计划列表响应模型"""
    items: list[PlanResponse]
    total: int
    page: int
    page_size: int

class TodayPlanDrugResponse(BaseModel):
    """今日计划药品响应模型"""
    id: int
    dosage: str
    drug: DrugBaseResponse

class TodayPlanItemResponse(BaseModel):
    """今日计划项响应模型"""
    plan: dict
    time_point: str
    drugs: list[TodayPlanDrugResponse]
    taken: bool

class TodayPlansResponse(BaseModel):
    """今日计划响应模型"""
    date: str
    plans: list[TodayPlanItemResponse]

class TrackResponse(BaseModel):
    """用药记录响应模型"""
    track_id: int
    created_at: datetime

# ========= 辅助函数 =========
def build_plan_drug_response(plan_drug: PlanDrug) -> PlanDrugResponse:
    """构建计划关联药品响应"""
    return PlanDrugResponse(
        id=plan_drug.id,
        plan_id=plan_drug.plan_id,
        drug_id=plan_drug.drug_id,
        dosage=plan_drug.dosage,
        drug=DrugBaseResponse(
            id=plan_drug.drug.id,
            name=plan_drug.drug.name,
            usage_method=plan_drug.drug.usage_method,
            image=plan_drug.drug.image
        )
    )

def build_plan_response(plan: Plan) -> PlanResponse:
    """构建计划响应"""
    # noinspection PyTypeChecker
    return PlanResponse(
        id=plan.id,
        user_id=plan.user_id,
        name=plan.name,
        plan_type=plan.plan_type,
        start_date=plan.start_date,
        end_date=plan.end_date,
        frequency_type=plan.frequency_type,
        frequency_detail=plan.frequency_detail,
        time_points=plan.time_points,
        sms_enabled=plan.sms_enabled,
        status=plan.status,
        created_at=plan.created_at,
        updated_at=plan.updated_at,
        drugs=[build_plan_drug_response(pd) for pd in plan.plan_drugs]
    )

# ========= 路由端点定义 =========
@router.get(
    "",
    response_model=PaginatedPlansResponse,
    responses={
        401: {"description": "未登录或token无效"}
    }
)
async def get_plans(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    status_filter: Optional[str] = Query(None, alias="status", description="状态筛选"),
    plan_type: Optional[str] = Query(None, description="类型筛选"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """
    获取计划列表接口

    - **page**: 页码，默认1
    - **page_size**: 每页数量，默认10，最大100
    - **status**: 状态筛选（active/paused/completed）
    - **plan_type**: 类型筛选（长期/周期）
    - **keyword**: 搜索关键词（计划名称）
    """
    query = db.query(Plan).filter(Plan.user_id == user_id)

    # 状态筛选
    if status_filter:
        query = query.filter(Plan.status == status_filter)

    # 类型筛选
    if plan_type:
        query = query.filter(Plan.plan_type == plan_type)

    # 关键词筛选
    if keyword:
        query = query.filter(Plan.name.ilike(f"%{keyword}%"))

    # 获取总数
    total = query.count()

    # 分页
    offset = (page - 1) * page_size
    plans = query.order_by(Plan.created_at.desc()).offset(offset).limit(page_size).all()

    # 加载关联数据
    for plan in plans:
        _ = plan.plan_drugs

    return PaginatedPlansResponse(
        items=[build_plan_response(plan) for plan in plans], # noqa
        total=total,
        page=page,
        page_size=page_size
    )

@router.get(
    "/{plan_id}",
    response_model=PlanResponse,
    responses={
        401: {"description": "未登录或token无效"},
        404: {"description": "计划不存在"}
    }
)
async def get_plan(
    plan_id: int,
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """
    获取计划详情接口

    - **plan_id**: 计划ID
    """
    plan: Plan | None = db.query(Plan).filter(
        Plan.id == plan_id,
        Plan.user_id == user_id
    ).first()

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="计划不存在"
        )

    # 加载关联数据
    _ = plan.plan_drugs

    return build_plan_response(plan)


@router.post(
    "",
    response_model=PlanResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        401: {"description": "未登录或token无效"}
    }
)
async def create_plan(
    request: CreatePlanRequest,
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """
    创建计划接口

    - **name**: 计划名称
    - **plan_type**: 计划类型（长期/周期）
    - **start_date**: 开始日期
    - **end_date**: 结束日期（周期计划必填）
    - **frequency_type**: 频率类型（daily/alternate/weekly/monthly）
    - **frequency_detail**: 频率详情
    - **time_points**: 每日用药时间点数组
    - **sms_enabled**: 是否启用短信提醒
    - **drug_ids**: 关联药品列表
    """
    # 验证药品存在且属于当前用户
    for drug_req in request.drug_ids:
        drug: Drug | None = db.query(Drug).filter(
            Drug.id == drug_req.drug_id,
            Drug.user_id == user_id
        ).first()
        if not drug:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"药品ID {drug_req.drug_id} 不存在"
            )

    # 创建计划
    # noinspection PyTypeChecker
    plan = Plan(
        user_id=user_id,
        name=request.name,
        plan_type=request.plan_type,
        start_date=request.start_date,
        end_date=request.end_date,
        frequency_type=request.frequency_type,
        frequency_detail=request.frequency_detail,
        time_points=request.time_points,
        sms_enabled=request.sms_enabled,
        status="active"
    )
    db.add(plan)
    db.flush()  # 获取plan.id

    # 添加关联药品
    for drug_req in request.drug_ids:
        plan_drug = PlanDrug(
            plan_id=plan.id,
            drug_id=drug_req.drug_id,
            dosage=drug_req.dosage
        )
        db.add(plan_drug)

    db.commit()
    db.refresh(plan)

    # 加载关联数据
    _ = plan.plan_drugs

    return build_plan_response(plan)


@router.put(
    "/{plan_id}",
    response_model=PlanResponse,
    responses={
        401: {"description": "未登录或token无效"},
        404: {"description": "计划不存在"}
    }
)
async def update_plan(
    plan_id: int,
    request: UpdatePlanRequest,
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """
    更新计划接口

    - **plan_id**: 计划ID
    - 请求体所有字段均为可选
    """
    plan: Plan | None = db.query(Plan).filter(
        Plan.id == plan_id,
        Plan.user_id == user_id
    ).first()

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="计划不存在"
        )

    # 更新字段 (只更新提供的字段)
    if request.name is not None:
        plan.name = request.name
    if request.plan_type is not None:
        plan.plan_type = request.plan_type
    if request.start_date is not None:
        plan.start_date = request.start_date
    if request.end_date is not None:
        plan.end_date = request.end_date
    if request.frequency_type is not None:
        plan.frequency_type = request.frequency_type
    if request.frequency_detail is not None:
        plan.frequency_detail = request.frequency_detail # noqa
    if request.time_points is not None:
        plan.time_points = request.time_points
    if request.sms_enabled is not None:
        plan.sms_enabled = request.sms_enabled

    # 更新关联药品
    if request.drug_ids is not None:
        # 验证药品存在且属于当前用户
        for drug_req in request.drug_ids:
            drug: Drug | None = db.query(Drug).filter(
                Drug.id == drug_req.drug_id,
                Drug.user_id == user_id
            ).first()
            if not drug:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"药品ID {drug_req.drug_id} 不存在"
                )

        # 删除旧的关联
        db.query(PlanDrug).filter(PlanDrug.plan_id == plan_id).delete()

        # 添加新的关联
        for drug_req in request.drug_ids:
            plan_drug = PlanDrug(
                plan_id=plan.id,
                drug_id=drug_req.drug_id,
                dosage=drug_req.dosage
            )
            db.add(plan_drug)

    plan.updated_at = datetime.now()
    db.commit()
    db.refresh(plan)

    # 加载关联数据
    _ = plan.plan_drugs

    return build_plan_response(plan)


@router.delete(
    "/{plan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"description": "未登录或token无效"},
        404: {"description": "计划不存在"}
    }
)
async def delete_plan(
    plan_id: int,
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """
    删除计划接口

    - **plan_id**: 计划ID
    """
    plan: Plan | None = db.query(Plan).filter(
        Plan.id == plan_id,
        Plan.user_id == user_id
    ).first()

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="计划不存在"
        )

    # 删除关联的PlanDrug
    db.query(PlanDrug).filter(PlanDrug.plan_id == plan_id).delete()

    # 删除关联的Track
    db.query(Track).filter(Track.plan_id == plan_id).delete()

    # 删除计划
    db.delete(plan)
    db.commit()

    return None


@router.post(
    "/{plan_id}/pause",
    response_model=PlanResponse,
    responses={
        401: {"description": "未登录或token无效"},
        404: {"description": "计划不存在"}
    }
)
async def pause_plan(
    plan_id: int,
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """
    暂停计划接口

    - **plan_id**: 计划ID
    """
    plan: Plan | None = db.query(Plan).filter(
        Plan.id == plan_id,
        Plan.user_id == user_id
    ).first()

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="计划不存在"
        )

    plan.status = "paused"
    plan.updated_at = datetime.now()
    db.commit()
    db.refresh(plan)

    # 加载关联数据
    _ = plan.plan_drugs

    return build_plan_response(plan)


@router.post(
    "/{plan_id}/resume",
    response_model=PlanResponse,
    responses={
        401: {"description": "未登录或token无效"},
        404: {"description": "计划不存在"}
    }
)
async def resume_plan(
    plan_id: int,
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """
    恢复计划接口

    - **plan_id**: 计划ID
    """
    plan: Plan | None = db.query(Plan).filter(
        Plan.id == plan_id,
        Plan.user_id == user_id
    ).first()

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="计划不存在"
        )

    plan.status = "active"
    plan.updated_at = datetime.now()
    db.commit()
    db.refresh(plan)

    # 加载关联数据
    _ = plan.plan_drugs

    return build_plan_response(plan)


@router.post(
    "/{plan_id}/complete",
    response_model=PlanResponse,
    responses={
        401: {"description": "未登录或token无效"},
        404: {"description": "计划不存在"}
    }
)
async def complete_plan(
    plan_id: int,
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """
    完成计划接口

    - **plan_id**: 计划ID
    """
    plan: Plan | None = db.query(Plan).filter(
        Plan.id == plan_id,
        Plan.user_id == user_id
    ).first()

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="计划不存在"
        )

    plan.status = "completed"
    plan.updated_at = datetime.now()
    db.commit()
    db.refresh(plan)

    # 加载关联数据
    _ = plan.plan_drugs

    return build_plan_response(plan)


@router.get(
    "/today",
    response_model=TodayPlansResponse,
    responses={
        401: {"description": "未登录或token无效"}
    }
)
async def get_today_plans(
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """
    获取今日计划接口
    """
    today = date.today()
    today_str = today.isoformat()

    # 获取所有active或paused状态的计划
    plans = db.query(Plan).filter(
        Plan.user_id == user_id,
        Plan.status.in_(["active", "paused"])
    ).all()

    today_plans = []

    for plan in plans:
        # 检查计划是否在有效期内
        if plan.start_date.date() > today:
            continue
        if plan.end_date and plan.end_date.date() < today:
            continue

        # 根据frequency_type判断今日是否需要执行
        should_execute_today = True

        if plan.frequency_type == "weekly" and plan.frequency_detail:
            weekdays = plan.frequency_detail.get("weekdays", [])
            if weekdays and today.weekday() + 1 not in weekdays:  # weekday()返回0-6，转换为1-7
                should_execute_today = False
        elif plan.frequency_type == "monthly" and plan.frequency_detail:
            days_of_month = plan.frequency_detail.get("days_of_month", [])
            if days_of_month and today.day not in days_of_month:
                should_execute_today = False
        elif plan.frequency_type == "alternate" and plan.frequency_detail:
            interval_days = plan.frequency_detail.get("interval_days", 1)
            if plan.start_date.date() > today:
                should_execute_today = False
            elif (today - plan.start_date.date()).days % interval_days != 0:
                should_execute_today = False

        if not should_execute_today:
            continue

        # 加载关联药品
        _ = plan.plan_drugs

        # 对每个时间点生成记录
        for time_point in plan.time_points:
            # 检查今日该时间点是否已服药
            track = db.query(Track).filter(
                Track.plan_id == plan.id,
                Track.user_id == user_id,
                Track.taken == True
            ).first()

            today_plans.append(TodayPlanItemResponse(
                plan={
                    "id": plan.id,
                    "name": plan.name,
                    "time_points": plan.time_points
                },
                time_point=time_point,
                drugs=[
                    TodayPlanDrugResponse(
                        id=pd.id,
                        dosage=pd.dosage,
                        drug=DrugBaseResponse(
                            id=pd.drug.id,
                            name=pd.drug.name,
                            usage_method=pd.drug.usage_method,
                            image=pd.drug.image
                        )
                    )
                    for pd in plan.plan_drugs
                ],
                taken=track is not None
            ))

    return TodayPlansResponse(
        date=today_str,
        plans=today_plans
    )

@router.post(
    "/{plan_id}/track",
    response_model=TrackResponse,
    responses={
        401: {"description": "未登录或token无效"},
        404: {"description": "计划不存在"}
    }
)
async def track_medication(
    plan_id: int,
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """
    记录用药接口

    - **plan_id**: 计划ID
    - **time_point**: 用药时间点（如"08:00"）
    """
    plan: Plan | None = db.query(Plan).filter(
        Plan.id == plan_id,
        Plan.user_id == user_id
    ).first()

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="计划不存在"
        )

    # 创建用药记录
    track = Track(
        user_id=user_id,
        plan_id=plan_id,
        taken=True,
        taken_at=datetime.now()
    )
    db.add(track)
    db.commit()
    db.refresh(track)

    return TrackResponse(
        track_id=track.id,
        created_at=track.created_at
    )


@router.delete(
    "/{plan_id}/track/{track_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"description": "未登录或token无效"},
        404: {"description": "记录不存在"}
    }
)
async def untrack_medication(
    plan_id: int,
    track_id: int,
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """
    取消用药记录接口

    - **plan_id**: 计划ID
    - **track_id**: 记录ID
    """
    track: Track | None = db.query(Track).filter(
        Track.id == track_id,
        Track.plan_id == plan_id,
        Track.user_id == user_id
    ).first()

    if not track:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="记录不存在"
        )

    db.delete(track)
    db.commit()

    return None
