from typing import List, Optional

from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Product
from app.repositories.product import ProductRepository
from app.repositories.product_category import ProductCategoryRepository
from app.schemas.brand import TopBrandResponse


class ProductService:
    async def search(
        self,
        db: AsyncSession,
        product_category_repo: ProductCategoryRepository,
        product_repo: ProductRepository,
        q: Optional[str] = None,
        brand_ids: Optional[List[int]] = None,
        category_ids: Optional[List[int]] = None,
    ) -> Sequence[Product]:

        filtered_product_ids = None
        if category_ids:
            filtered_product_ids = await product_category_repo.get_product_ids_by_categories(
                db, category_ids
            )
            if not filtered_product_ids:
                return []

        filters = {}
        if brand_ids:
            filters["brand_id"] = brand_ids

        products = await product_repo.get_alike_with_filters(
            db=db,
            q=q,
            ids=filtered_product_ids,
            filters=filters,
        )

        return products

    async def get_top_brands_by_query(
            self,
            db: AsyncSession,
            repo: ProductRepository,
            q: str,
    ):
        rows = await repo.get_top_brands_by_query(db, q)

        return [
            TopBrandResponse(brand_id=brand_id, total=total, brand_name=brand_name)
            for brand_id, brand_name, total in rows
        ]
