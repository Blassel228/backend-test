from typing import List

from fastapi import APIRouter, Query

from app.api.dependencies import (
    get_db_dep,
    product_category_dep,
    product_category_repository_dep,
)
from app.schemas.brand import BrandCount
from app.schemas.product_category import TopCategoryResponse, CategoryCount

router = APIRouter()


@router.get("/top-categories", response_model=List[TopCategoryResponse])
async def top_categories(
    service: product_category_dep,
    db: get_db_dep,
    repo: product_category_repository_dep,
    q: str = Query(..., min_length=1),
) -> list[BrandCount]:
    return await service.get_top_categories_by_query(db=db, q=q, repo=repo)


@router.get("/categories-count", response_model=List[CategoryCount])
async def count_categories(
    service: product_category_dep,
    db: get_db_dep,
    repo: product_category_repository_dep,
    category_ids: List[int] = Query(...),
    brand_ids: List[int] = Query(None),
    q: str = Query(..., min_length=1),
) -> list[CategoryCount]:
    return await service.count_categories(
        q=q, db=db, repo=repo, category_ids=category_ids, brand_ids=brand_ids
    )
