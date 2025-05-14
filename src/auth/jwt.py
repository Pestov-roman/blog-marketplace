from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt

from src.auth.roles import Role
from src.settings import settings

ALGORITHM = "HS256"


def create_access_token(user_id: str, role: Role | str) -> str:
    if isinstance(role, Role):
        role = role.value
    to_encode = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.now(UTC) + timedelta(minutes=settings.jwt_expires_minutes),
    }
    encoded: str = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=ALGORITHM)
    return encoded


def verify_token(token: str) -> dict[str, Any] | None:
    try:
        decoded: dict[str, Any] = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[ALGORITHM]
        )
        return decoded
    except JWTError:
        return None
