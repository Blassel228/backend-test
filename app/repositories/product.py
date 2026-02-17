from app.models import Product, Brand
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
    ) -> list[tuple[int, str, int]]:

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