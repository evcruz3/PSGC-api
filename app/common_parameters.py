from typing import Optional
from pydantic import BaseModel, Field
from fastapi import Depends

class CommonQueryParams(BaseModel):
    skip: int = Field(0, description="Number of items to skip for pagination")
    limit: int = Field(20, description="Maximum number of items to return")
    q: Optional[str] = Field(..., description="Filter conditions")

async def common_parameters(q: str | None = None, page: int = 1, page_size: int = 20):
    # return {"q": q, "skip": (page - 1) * page_size, "limit": page_size}
    return CommonQueryParams(q=q, skip=(page - 1) * page_size, limit=page_size)

CommonsDep = Depends(common_parameters)

