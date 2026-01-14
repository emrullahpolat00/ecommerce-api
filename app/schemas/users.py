from pydantic import BaseModel, EmailStr
from app.schemas.common import ORMBase

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str

class UserUpdate(BaseModel):
    full_name: str | None = None

class UserOut(ORMBase):
    id: int
    email: str
    full_name: str