from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.product import ProductRepository
from app.repositories.product_category import ProductCategoryRepository
from app.services.product import ProductService
from app.services.product_category import ProductCategoryService
from app.utils.deps import get_db

get_db_dep = Annotated[AsyncSession, Depends(get_db)]

product_repository_dep = Annotated[ProductRepository, Depends(ProductRepository)]
product_category_repository_dep = Annotated[ProductCategoryRepository, Depends(ProductCategoryRepository)]

product_service_dep = Annotated[ProductService, Depends(ProductService)]
product_category_dep = Annotated[ProductCategoryService, Depends(ProductCategoryService)]