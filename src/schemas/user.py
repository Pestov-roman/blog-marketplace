from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserRegisterIn(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime

    model_config = {"from_attributes": True}
