from functools import wraps
from typing import Callable

from fastapi import Depends

from src.auth.roles import Role


def require_roles(*roles: Role):
    def decorator(endpoint: Callable):
        endpoint.dependencies = getattr(endpoint, "dependencies", []) + Depends(
            require_roles(*roles)
        )
        return wraps(endpoint)(endpoint)

    return decorator
