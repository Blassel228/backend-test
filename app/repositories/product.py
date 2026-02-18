from app.models import Product, Brand, ProductCategory
from app.repositories.base import BaseRepository

from typing import Optional, List, Dict, Any, Sequence
from sqlalchemy import select, and_, func, desc
from sqlalchemy.ext.asyncio import AsyncSession


class ProductRepository(BaseRepository):
    model = Product

    async def get_alike_with_filters(
        self,
        db: AsyncSession,
        q: str,
        ids: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Sequence[Product]:
        stmt = select(self.model)
        conditions = []

        if q:
            conditions.append(self.model.name.ilike(f"%{q}%"))

        if ids:
            conditions.append(self.model.id.in_(ids))

        if filters:
            conditions.extend(self.build_filters(filters))

        if conditions:
            stmt = stmt.where(and_(*conditions))

        result = await db.scalars(stmt)
        return result.all()

    async def get_top_brands_by_query(
        self,
        db: AsyncSession,
        q: str,
        limit: int = 10,
    ) -> Sequence:
        stmt = (
            select(
                self.model.brand_id,
                Brand.name.label("brand_name"),
                func.count(self.model.id).label("total"),
            )
            .join(Brand, Brand.id == self.model.brand_id)
            .where(self.model.name.ilike(f"%{q}%"))
            .group_by(self.model.brand_id, Brand.name)
            .order_by(desc("total"))
            .limit(limit)
        )

        result = await db.execute(stmt)
        return result.all()

    async def count_brands(
        self,
        db: AsyncSession,
        q: str,
        category_ids: list[int],
        brand_ids: list[int],
    ) -> Sequence:
        stmt = (
            select(Product.brand_id, func.count(Product.id).label("count"))
            .where(Product.name.ilike(f"%{q}%"))
            .where(Product.brand_id.in_(brand_ids))
        )

        if category_ids:
            stmt = stmt.join(ProductCategory, ProductCategory.product_id == Product.id).where(ProductCategory.category_id.in_(category_ids))

        stmt = stmt.group_by(Product.brand_id)

        result = await db.execute(stmt)
        return result.all()
