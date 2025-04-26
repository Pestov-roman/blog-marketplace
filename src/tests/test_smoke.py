import httpx
import pytest

from src.app.main import app


@pytest.mark.asyncio
async def test_health():
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        r = await client.get("/health")
        assert r.status_code == 200
