"""
药品管理模块，包含药品的CRUD和外部药品搜索接口
"""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from ..core import get_db, get_user_id
from ..models import Drug

# ========= 初始化路由对象 =========
router = APIRouter()

# ========= 请求/响应模型定义 =========
# 1. 请求模型
class CreateDrugRequest(BaseModel):
    """创建药品请求模型"""
    name: str
    image: Optional[str] = None
    usage_method: str
    dosage: str
    remaining: Optional[str] = None
    source: str
    external_id: Optional[int] = None

class UpdateDrugRequest(BaseModel):
    """更新药品请求模型"""
    name: Optional[str] = None
    image: Optional[str] = None
    usage_method: Optional[str] = None
    dosage: Optional[str] = None
    remaining: Optional[str] = None
    source: Optional[str] = None
    external_id: Optional[int] = None

class DrugCreateRequest(BaseModel):
    """创建计划时关联药品的请求模型"""
    drug_id: int
    dosage: str

# 2. 响应模型
class DrugResponse(BaseModel):
    """药品响应模型"""
    id: int
    user_id: int
    name: str
    image: Optional[str]
    usage_method: str
    dosage: str
    remaining: Optional[str]
    source: str
    external_id: Optional[int]
    created_at: datetime
    updated_at: datetime

class PaginatedDrugsResponse(BaseModel):
    """分页药品列表响应模型"""
    items: list[DrugResponse]
    total: int

# ========= 路由端点定义 =========
@router.get(
    "",
    response_model=PaginatedDrugsResponse,
    responses={
        401: {"description": "未登录或token无效"},
        403: {"description": "账户已被禁用"}
    }
)
async def get_drugs(
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    usage_method: Optional[str] = Query(None, description="用法筛选"),
    source: Optional[str] = Query(None, description="来源筛选"),
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """
    获取药品列表接口

    - **keyword**: 搜索关键词（药品名称）
    - **usage_method**: 用法筛选（口服/注射/外用/含服/吸入/滴入/其他）
    - **source**: 来源筛选（医疗数据库/手动输入）
    """
    # 构建查询
    query = db.query(Drug).filter(Drug.user_id == user_id)

    # 关键词筛选
    if keyword:
        query = query.filter(Drug.name.ilike(f"%{keyword}%"))

    # 用法筛选
    if usage_method:
        query = query.filter(Drug.usage_method == usage_method)

    # 来源筛选
    if source:
        query = query.filter(Drug.source == source)

    # 获取总数
    total = query.count()
    drugs = query.order_by(Drug.created_at.desc()).all()

    # noinspection PyTypeChecker
    return PaginatedDrugsResponse(
        items=[DrugResponse(
            id=drug.id,
            user_id=drug.user_id,
            name=drug.name,
            image=drug.image,
            usage_method=drug.usage_method,
            dosage=drug.dosage,
            remaining=drug.remaining,
            source=drug.source,
            external_id=drug.external_id,
            created_at=drug.created_at,
            updated_at=drug.updated_at
        ) for drug in drugs],
        total=total
    )

@router.get(
    "/search",
    response_model=list[DrugResponse],
    responses={
        401: {"description": "未登录或token无效"}
    }
)
async def search_external_drugs(
    keyword: str = Query(..., description="搜索关键词"),
    user_id: int = Depends(get_user_id)
):
    """
    搜索外部药品接口

    - **keyword**: 搜索关键词

    注意: 此接口为模拟接口,实际应调用外部医疗数据库API
    """
    # 模拟外部药品数据库搜索结果
    # 实际项目中应替换为真实的外部API调用
    # 根据关键词返回更真实的模拟数据
    usage_methods = ["口服", "注射", "外用", "含服", "吸入", "滴入"]
    dosages = ["1粒", "2粒", "1片", "2片", "1支", "2支", "10ml", "20ml"]

    mock_results = []
    base_id = 1000

    # 生成3-5个模拟结果
    import random
    count = random.randint(3, 5)

    for i in range(count):
        mock_results.append({
            "id": base_id + i,
            "user_id": user_id,
            "name": f"{keyword}{['胶囊', '片剂', '颗粒', '口服液', '注射液', '软膏'][i % 6]}",
            "image": None,
            "usage_method": random.choice(usage_methods),
            "dosage": random.choice(dosages),
            "remaining": None,
            "source": "医疗数据库",
            "external_id": base_id + i,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        })

    return [DrugResponse(**item) for item in mock_results]


@router.get(
    "/{drug_id}",
    response_model=DrugResponse,
    responses={
        401: {"description": "未登录或token无效"},
        404: {"description": "药品不存在"}
    }
)
async def get_drug(
    drug_id: int,
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """
    获取药品详情接口

    - **drug_id**: 药品ID
    """
    drug: Drug | None = db.query(Drug).filter(
        Drug.id == drug_id,
        Drug.user_id == user_id
    ).first()

    if not drug:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="药品不存在"
        )

    # noinspection PyTypeChecker
    return DrugResponse(
        id=drug.id,
        user_id=drug.user_id,
        name=drug.name,
        image=drug.image,
        usage_method=drug.usage_method,
        dosage=drug.dosage,
        remaining=drug.remaining,
        source=drug.source,
        external_id=drug.external_id,
        created_at=drug.created_at,
        updated_at=drug.updated_at
    )

@router.post(
    "",
    response_model=DrugResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        401: {"description": "未登录或token无效"}
    }
)
async def create_drug(
    request: CreateDrugRequest,
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """
    创建药品接口

    - **name**: 药品名称
    - **image**: 药品图片(Base64)
    - **usage_method**: 用法
    - **dosage**: 用量
    - **remaining**: 余量
    - **source**: 来源（医疗数据库/手动输入）
    - **external_id**: 外部数据库ID
    """
    drug = Drug(
        user_id=user_id,
        name=request.name,
        image=request.image or "",
        usage_method=request.usage_method,
        dosage=request.dosage,
        remaining=request.remaining,
        source=request.source,
        external_id=request.external_id
    )
    db.add(drug)
    db.commit()
    db.refresh(drug)

    # noinspection PyTypeChecker
    return DrugResponse(
        id=drug.id,
        user_id=drug.user_id,
        name=drug.name,
        image=drug.image,
        usage_method=drug.usage_method,
        dosage=drug.dosage,
        remaining=drug.remaining,
        source=drug.source,
        external_id=drug.external_id,
        created_at=drug.created_at,
        updated_at=drug.updated_at
    )


@router.put(
    "/{drug_id}",
    response_model=DrugResponse,
    responses={
        401: {"description": "未登录或token无效"},
        404: {"description": "药品不存在"}
    }
)
async def update_drug(
    drug_id: int,
    request: UpdateDrugRequest,
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """
    更新药品接口

    - **drug_id**: 药品ID
    - 请求体所有字段均为可选
    """
    drug: Drug | None = db.query(Drug).filter(
        Drug.id == drug_id,
        Drug.user_id == user_id
    ).first()

    if not drug:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="药品不存在"
        )

    # 更新字段（只更新提供的字段）
    if request.name is not None:
        drug.name = request.name
    if request.image is not None:
        drug.image = request.image
    if request.usage_method is not None:
        drug.usage_method = request.usage_method
    if request.dosage is not None:
        drug.dosage = request.dosage
    if request.remaining is not None:
        drug.remaining = request.remaining
    if request.source is not None:
        drug.source = request.source
    if request.external_id is not None:
        drug.external_id = request.external_id

    drug.updated_at = datetime.now()
    db.commit()
    db.refresh(drug)

    # noinspection PyTypeChecker
    return DrugResponse(
        id=drug.id,
        user_id=drug.user_id,
        name=drug.name,
        image=drug.image,
        usage_method=drug.usage_method,
        dosage=drug.dosage,
        remaining=drug.remaining,
        source=drug.source,
        external_id=drug.external_id,
        created_at=drug.created_at,
        updated_at=drug.updated_at
    )


@router.delete(
    "/{drug_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"description": "未登录或token无效"},
        404: {"description": "药品不存在"}
    }
)
async def delete_drug(
    drug_id: int,
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db)
):
    """
    删除药品接口

    - **drug_id**: 药品ID
    """
    drug: Drug | None = db.query(Drug).filter(
        Drug.id == drug_id,
        Drug.user_id == user_id
    ).first()

    if not drug:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="药品不存在"
        )

    db.delete(drug)
    db.commit()

    return None


