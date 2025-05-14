from pydantic import BaseModel


class LoginIn(BaseModel):
    email: str
    password: str
    role: str | None = None


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
