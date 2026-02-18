from pydantic import BaseModel


class TopCategoryResponse(BaseModel):
    total: int
    category_name: str
    category_id: int


class CategoryCount(BaseModel):
    category_id: int
    count: int
