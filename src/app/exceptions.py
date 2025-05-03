from typing import Any, Dict

from fastapi import HTTPException, status


class AppError(HTTPException):
    def __init__(
        self, status_code: int, detail: str | Dict[str, Any], *, code: str = "app_error"
    ):
        self.code = code
        super().__init__(status_code=status_code, detail=detail)


class NotFoundError(AppError):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ForbiddenError(AppError):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
