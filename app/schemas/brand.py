from pydantic import BaseModel


class TopBrandResponse(BaseModel):
    total: int
    brand_id: int
    brand_name: str