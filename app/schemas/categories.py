from pydantic import BaseModel
from app.schemas.common import ORMBase

class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str | None = None

class CategoryOut(ORMBase):
    id: int
    name: str