from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.product_category import ProductCategoryRepository
from app.schemas.product_category import TopCategoryResponse


class ProductCategoryService:
    async def get_top_categories_by_query(self, q: str, db: AsyncSession, repo: ProductCategoryRepository, limit: Optional[int] = 10):
        rows = await repo.get_top_categories_by_query(db, q, limit=limit)

        return [
            TopCategoryResponse(brand_id=brand_id, total=total, category_name=category_name)
            for brand_id, category_name, total  in rows
        ]
