from fastapi.security import HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from src.auth.jwt import verify_token

header_scheme = HTTPBearer(auto_error=False)


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        token = request.cookies.get("access_token")
        if not token:
            header = await header_scheme(request)
            if header:
                token = header.credentials

        if token and verify_token(token):
            request.state.user_sub = verify_token(token)
        return await call_next(request)
