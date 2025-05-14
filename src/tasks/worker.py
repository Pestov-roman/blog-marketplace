from __future__ import annotations

from src.infrastructure.celery_app import celery_app


@celery_app.task(name="health_check")  # type: ignore[misc]
def health_check() -> str:
    return "Celery is working fine!"
