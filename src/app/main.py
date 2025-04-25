from fastapi import FastAPI

from src.api.v1 import categories
from src.settings import settings

app = FastAPI(title="Blog Marketplace", version="0.1.0", debug=settings.debug)
app.include_router(categories.router)
