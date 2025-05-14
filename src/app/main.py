from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse

from src.api.v1 import articles, auth, categories, uploads
from src.infrastructure.logging import configure_logging
from src.middleware.auth import AuthMiddleware
from src.middleware.error_handler import ErrorMiddleware
from src.settings import settings

configure_logging()

app = FastAPI(title="Blog Marketplace", version="0.1.0", debug=settings.debug)
app.add_middleware(ErrorMiddleware)
app.add_middleware(AuthMiddleware)

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(auth.router)
api_v1_router.include_router(categories.router)
api_v1_router.include_router(articles.router)
api_v1_router.include_router(uploads.router)

app.include_router(api_v1_router)


@app.get("/health")
async def health_check() -> JSONResponse:
    return JSONResponse(content={"status": "ok"}, status_code=200)
