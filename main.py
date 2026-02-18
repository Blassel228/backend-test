from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, ForeignKey, select, func
from sqlalchemy.sql import text

DATABASE_URL = ""

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

app = FastAPI()


class CategoryFacet(BaseModel):
    category_id: int
    category_name: str
    count: int


from sqlalchemy import MetaData

metadata = MetaData()

product_categories = Table(
    "product_categories",
    metadata,
    Column("category_id", Integer, ForeignKey("categories.id")),
    Column("product_id", Integer, ForeignKey("products.id")),
)

products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("brand_id", Integer),
)

categories = Table(
    "categories",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
)


async def get_category_facets(
    q: Optional[str] = None, brand_ids: Optional[List[int]] = None
) -> List[CategoryFacet]:
    async with AsyncSessionLocal() as session:
        stmt = (
            select(
                product_categories.c.category_id,
                categories.c.name.label("category_name"),
                func.count(product_categories.c.product_id).label("count"),
            )
            .join(products, products.c.id == product_categories.c.product_id)
            .join(categories, categories.c.id == product_categories.c.category_id)
        )

        if q:
            stmt = stmt.where(products.c.name.ilike(f"%{q}%"))
        if brand_ids:
            stmt = stmt.where(products.c.brand_id.in_(brand_ids))

        stmt = stmt.group_by(product_categories.c.category_id, categories.c.name)
        stmt = stmt.order_by(text("count DESC"))

        result = await session.execute(stmt)
        rows = result.fetchall()
        return [
            CategoryFacet(
                category_id=r.category_id, category_name=r.category_name, count=r.count
            )
            for r in rows
        ]


@app.get("/category-facets", response_model=List[CategoryFacet])
async def category_facets(
    q: Optional[str] = Query(None), brandIds: Optional[List[int]] = Query(None)
):
    return await get_category_facets(q=q, brand_ids=brandIds)
