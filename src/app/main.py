from fastapi import FastAPI

from src.api.v1 import articles, auth, categories
from src.middleware.auth import AuthMiddleware
from src.settings import settings

app = FastAPI(title="Blog Marketplace", version="0.1.0", debug=settings.debug)
app.add_middleware(AuthMiddleware)
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(articles.router)
