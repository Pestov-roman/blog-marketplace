from datetime import datetime, timedelta
from uuid import UUID

from jose import JWTError, jwt
from settings.base import settings

ALGORITHM = "HS256"


def create_access_token(sub: str | UUID) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.jwt_exp_minutes)
    payload = {
        "sub": str(sub),
        "exp": expire,
    }
    encoded_jwt = jwt.encode(payload, settings.jwt_secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
