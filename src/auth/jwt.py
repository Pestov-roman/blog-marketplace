from datetime import datetime, timedelta
from typing import Any

from jose import jwt

from src.auth.roles import Role
from src.settings import settings

ALGORITHM = "HS256"


def create_access_token(user_id: str, role: Role | str) -> str:
    if isinstance(role, Role):
        role = role.value
    to_encode = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=settings.jwt_expires_minutes),
    }
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=ALGORITHM)


def verify_token(token: str) -> dict[str, Any] | None:
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[ALGORITHM])
    except jwt.JWTError:
        return None
