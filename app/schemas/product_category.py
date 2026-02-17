from pydantic import BaseModel


class TopCategoryResponse(BaseModel):
    total: int
    category_name: str
    brand_id: int