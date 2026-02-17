from typing import List

from fastapi import APIRouter, Query

from app.api.dependencies import get_db_dep, product_category_dep, product_category_repository_dep
from app.schemas.product_category import TopCategoryResponse

router = APIRouter()


@router.get("/top-categories", response_model=List[TopCategoryResponse])
async def top_categories(
    service: product_category_dep,
    db: get_db_dep,
    repo: product_category_repository_dep,
    q: str = Query(..., min_length=1),
):
    return await service.get_top_categories_by_query(db=db, q=q, repo=repo)


