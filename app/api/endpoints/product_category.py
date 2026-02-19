import json
from typing import List, Optional

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
        brand_ids: Optional[List[int]] = Query(default=None),
        q: str = Query(..., min_length=1),
        selected_categories_with_counts: Optional[str] = Query(default=None),
) -> list[CategoryCount]:
    parsed_counts: Optional[dict[int, int]] = None

    if selected_categories_with_counts:
        try:
            data = json.loads(selected_categories_with_counts)
            print("data: ", data)
            parsed_counts = {int(k): v for k, v in data.items()}
        except (json.JSONDecodeError, ValueError, TypeError):
            parsed_counts = None

    print("selected_categories_with_counts: ", parsed_counts)

    return await service.count_categories(
        q=q,
        db=db,
        repo=repo,
        category_ids=category_ids,
        brand_ids=brand_ids,
        selected_categories_with_counts=parsed_counts,
    )