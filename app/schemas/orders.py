from pydantic import BaseModel, Field
from app.schemas.common import ORMBase

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class OrderCreate(BaseModel):
    user_id: int
    items: list[OrderItemCreate]

class OrderItemOut(ORMBase):
    product_id: int
    quantity: int

class OrderOut(ORMBase):
    id: int
    user_id: int
    items: list[OrderItemOut]