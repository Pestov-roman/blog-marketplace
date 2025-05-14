from __future__ import annotations

import structlog
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.auth.jwt import verify_token
from src.auth.roles import Role

log = structlog.get_logger(__name__)


class RoleGuardMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        token = request.cookies.get("access_token")
        if not token:
            request.state.user = {"id": None, "roles": Role.READER}
            return await call_next(request)
        try:
            payload = verify_token(token)
            if payload is None:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid token"},
                )
            request.state.user = {
                "id": payload["sub"],
                "roles": Role.from_str(payload["role"]),
            }
        except Exception as exc:
            log.warning("invalid-token", err=str(exc))
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid token"},
            )
        return await call_next(request)
