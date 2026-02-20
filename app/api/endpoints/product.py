from typing import Optional, List
from fastapi import APIRouter, Query

from app.api.dependencies import (
    get_db_dep,
    product_repository_dep,
    product_category_repository_dep,
    product_service_dep,
)
from app.schemas.brand import TopBrandResponse, BrandCount

router = APIRouter()


@router.get("/search")
async def search_products(
    product_repo: product_repository_dep,
    product_category_repo: product_category_repository_dep,
    service: product_service_dep,
    db: get_db_dep,
    offset: int = None,
    limit: int = None,
    q: Optional[str] = Query(None, description="Search query for product name"),
    brand_ids: Optional[List[int]] = Query(None, examples=[523]),
    category_ids: Optional[List[int]] = Query(None),
):
    products = await service.search(
        offset=offset,
        limit=limit,
        db=db,
        product_repo=product_repo,
        product_category_repo=product_category_repo,
        q=q,
        brand_ids=brand_ids,
        category_ids=category_ids,
    )

    total = await service.count_products_for_search(
        repo=product_repo,
        db=db,
        q=q,
        brand_ids=brand_ids,
        category_ids=category_ids,
    )

    return {"products": products, "total": total}


@router.get("/search/top-brands", response_model=List[TopBrandResponse])
async def top_brands(
    service: product_service_dep,
    repo: product_repository_dep,
    db: get_db_dep,
    q: Optional[str] = Query(None, description="Search query for product name"),
) ->  list[TopBrandResponse]:
    return await service.get_top_brands_by_query(db=db, repo=repo, q=q)


@router.get("/search/count-brands")
async def count_brands(
    service: product_service_dep,
    repo: product_repository_dep,
    db: get_db_dep,
    q: Optional[str] = Query(None, description="Search query for product name"),
    category_ids: List[int] = Query(None),
    brand_ids: List[int] = Query(...),
) -> list[BrandCount]:
    return await service.count_brands(
        repo=repo,
        db=db,
        q=q,
        category_ids=category_ids,
        brand_ids=brand_ids,
    )
