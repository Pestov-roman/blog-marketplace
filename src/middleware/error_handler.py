from typing import Awaitable, Callable

import structlog
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.app.exceptions import AppError

log = structlog.get_logger("error-handler")


class ErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        try:
            return await call_next(request)
        except AppError as exc:
            log.warning(
                "handled_error",
                path=request.url.path,
                code=exc.code,
                status_code=exc.status_code,
                detail=exc.detail,
            )
            return JSONResponse(
                status_code=exc.status_code,
                content={"error": exc.code, "detail": exc.detail},
            )
        except Exception:
            log.exception("unhandled_exception")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "internal_error",
                    "detail": "An unexpected error occurred",
                },
            )
