from typing import List, Optional

from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Product
from app.repositories.product import ProductRepository
from app.repositories.product_category import ProductCategoryRepository
from app.schemas.brand import TopBrandResponse, BrandCount


class ProductService:
    async def search(
        self,
        db: AsyncSession,
        product_category_repo: ProductCategoryRepository,
        product_repo: ProductRepository,
        q: Optional[str] = None,
        brand_ids: Optional[List[int]] = None,
        with_empty_brands: bool = True,
        category_ids: Optional[List[int]] = None,
        offset: int | None = None,
        limit: int | None= None,
    ) -> Sequence[Product]:
        filtered_product_ids = None
        if category_ids:
            filtered_product_ids = (
                await product_category_repo.get_product_ids_by_categories(
                    db, category_ids
                )
            )
            if not filtered_product_ids:
                return []

        filters = {}
        if brand_ids:
            filters["brand_id"] = brand_ids

        products = await product_repo.select_products_with_filters(
            db=db,
            q=q,
            filtered_product_ids=filtered_product_ids,
            with_empty_brands=with_empty_brands,
            brand_ids=brand_ids,
            offset=offset,
            limit=limit,
        )

        return products

    async def count_products_for_search(
        self,
        q: str,
        repo: ProductRepository,
        db: AsyncSession,
        brand_ids: List[int],
        category_ids: List[int],
    ) -> int:
        return await repo.count_total_products(
            db=db, q=q, brand_ids=brand_ids, category_ids=category_ids
        )

    async def get_top_brands_by_query(
        self,
        db: AsyncSession,
        repo: ProductRepository,
        q: str,
    ) -> list[TopBrandResponse]:
        rows = await repo.get_top_brands_by_query(db, q)

        return [
            TopBrandResponse(brand_id=brand_id, total=total, brand_name=brand_name)
            for brand_id, brand_name, total in rows
        ]

    async def count_brands(
        self,
        db: AsyncSession,
        repo: ProductRepository,
        q: str,
        category_ids: List[int],
        brand_ids: List[int],
    ) -> list[BrandCount]:
        rows = await repo.count_brands(
            db=db, q=q, category_ids=category_ids, brand_ids=brand_ids
        )

        return [BrandCount(count=count, brand_id=brand_id) for brand_id, count in rows]
