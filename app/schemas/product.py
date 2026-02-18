from typing import Optional, List

from pydantic import BaseModel


class SearchRequestParams(BaseModel):
    brand_ids: Optional[List[int]] = None
    category_ids: Optional[List[int]] = None
