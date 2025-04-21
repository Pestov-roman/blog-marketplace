from fastapi import FastAPI

from src.settings import settings

app = FastAPI(title="Blog Marketplace", version="0.1.0", debug=settings.debug)
