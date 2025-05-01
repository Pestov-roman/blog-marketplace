from fastapi import FastAPI
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
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(articles.router)
app.include_router(uploads.router)


@app.get("/health")
async def health_check() -> JSONResponse:
    return JSONResponse(content={"status": "ok"}, status_code=200)
