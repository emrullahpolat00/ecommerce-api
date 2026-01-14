from pydantic import BaseModel, Field
from app.schemas.common import ORMBase

class ProductCreate(BaseModel):
    name: str
    price: float = Field(gt=0)
    category_id: int

class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = Field(default=None, gt=0)
    category_id: int | None = None

class ProductOut(ORMBase):
    id: int
    name: str
    price: float
    category_id: int