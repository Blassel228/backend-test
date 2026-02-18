from fastapi import APIRouter
from app.api.endpoints import product
from app.api.endpoints import product_category

api_router = APIRouter(prefix="/api")

api_router.include_router(product.router, prefix="/product", tags=["Product"])
api_router.include_router(
    product_category.router, prefix="/product-category", tags=["Product Category"]
)
