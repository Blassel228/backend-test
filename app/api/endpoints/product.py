from typing import Optional, List
from fastapi import APIRouter, Query

from app.api.dependencies import get_db_dep, product_repository_dep, product_category_repository_dep, \
    product_service_dep
from app.schemas.brand import TopBrandResponse

router = APIRouter()

@router.get('/')
async def get_many(product_repo: product_repository_dep, db: get_db_dep):
    return await product_repo.get_many(db=db)

@router.get("/search")
async def search_products(
    product_repo: product_repository_dep,
    product_category_repo: product_category_repository_dep,
    service: product_service_dep,
    db: get_db_dep,
    q: Optional[str] = Query(None, description="Search query for product name"),
    brand_ids: Optional[List[int]] = Query(None, examples=[523]),
    category_ids: Optional[List[int]] = Query(None),
):
    products = await service.search(
        db=db,
        product_repo=product_repo,
        product_category_repo=product_category_repo,
        q=q,
        brand_ids=brand_ids,
        category_ids=category_ids,
    )
    return products

@router.get("/search/top-brands", response_model=list[TopBrandResponse])
async def top_brands(
    service: product_service_dep,
    repo: product_repository_dep,
    db: get_db_dep,
    q: str,
):
    return await service.get_top_brands_by_query(db=db, repo=repo, q=q)