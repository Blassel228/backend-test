from typing import List

from sqlalchemy import select, Sequence, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ProductCategory, Product, Category
from app.repositories.base import BaseRepository


class ProductCategoryRepository(BaseRepository):
    model = ProductCategory

    async def get_product_ids_by_categories(
        self, db: AsyncSession, category_ids: List[int]
    ) -> Sequence[ProductCategory]:
        stmt = select(self.model.product_id).where(
            self.model.category_id.in_(category_ids)
        )
        result = await db.scalars(stmt)
        return result.all()

    async def get_top_categories_by_query(
            self,
            db: AsyncSession,
            q: str,
            limit: int = 10,
    ) -> list[tuple[int, str, int]]:
        stmt = (
            select(
                self.model.category_id,
                Category.name.label("category_name"),
                func.count(self.model.product_id).label("total"),
            )
            .join(Product, Product.id == self.model.product_id)
            .join(Category, Category.id == self.model.category_id)
            .where(Product.name.ilike(f"%{q}%"))
            .group_by(self.model.category_id, Category.name)
            .order_by(desc("total"))
            .limit(limit)
        )

        result = await db.execute(stmt)
        return result.all()

