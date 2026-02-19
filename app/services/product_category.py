from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.product_category import ProductCategoryRepository
from app.schemas.product_category import TopCategoryResponse, CategoryCount


class ProductCategoryService:
    async def get_top_categories_by_query(
        self,
        q: str,
        db: AsyncSession,
        repo: ProductCategoryRepository,
        limit: Optional[int] = 10,
    ) -> list[TopCategoryResponse]:
        rows = await repo.get_top_categories_by_query(db, q, limit=limit)

        return [
            TopCategoryResponse(
                category_id=category_id, total=total, category_name=category_name
            )
            for category_id, category_name, total in rows
        ]

    async def count_categories(
        self,
        q: str,
        db: AsyncSession,
        repo: ProductCategoryRepository,
        category_ids: List[int],
        brand_ids: List[int],
        selected_categories_with_counts: dict[int, int] | None = None,
    ) -> list[CategoryCount]:
        rows = await repo.count_categories(
            q=q,
            db=db,
            category_ids=category_ids,
            brand_ids=brand_ids,
            selected_categories_with_counts=selected_categories_with_counts,
        )

        result = []

        if selected_categories_with_counts:
            for category_id, count in selected_categories_with_counts.items():
                result.append(CategoryCount(category_id=category_id, count=count))

        for category_id, count in rows:
            result.append(CategoryCount(category_id=category_id, count=count))

        return result
