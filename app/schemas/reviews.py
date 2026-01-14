from pydantic import BaseModel, Field
from app.schemas.common import ORMBase

class ReviewCreate(BaseModel):
    user_id: int
    product_id: int
    rating: int = Field(ge=1, le=5)
    comment: str | None = None

class ReviewUpdate(BaseModel):
    rating: int | None = Field(default=None, ge=1, le=5)
    comment: str | None = None

class ReviewOut(ORMBase):
    id: int
    user_id: int
    product_id: int
    rating: int
    comment: str | None