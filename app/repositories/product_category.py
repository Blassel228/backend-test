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
    ) -> Sequence:
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

    async def count_categories(
        self,
        db: AsyncSession,
        q: str,
        category_ids: List[int],
        brand_ids: List[int],
    ) -> Sequence:
        stmt = (
            select(
                Category.id.label("category_id"), func.count(Product.id).label("count")
            )
            .join(
                ProductCategory,
                ProductCategory.category_id == Category.id,
                isouter=True,
            )
            .join(Product, (Product.id == ProductCategory.product_id), isouter=True)
            .where(Category.id.in_(category_ids))
            .where(Product.name.ilike(f"%{q}%"))
        )

        if brand_ids:
            stmt = stmt.where(Product.brand_id.in_(brand_ids))

        stmt = stmt.group_by(Category.id)

        result = await db.execute(stmt)

        return result.all()
