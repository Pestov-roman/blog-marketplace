import logging

from celery import Celery
from celery.schedules import crontab

from src.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")
logger.info(f"Celery broker DSN: {settings.rabbitmq_dsn}")
celery_app = Celery(
    "blog-marketplace",
    broker=settings.rabbitmq_dsn,
    backend="rpc://",
    broker_connection_retry=True,
    broker_connection_retry_on_startup=True,
    broker_connection_max_retries=10,
    broker_connection_retry_delay=5,
)

celery_app.autodiscover_tasks(["src.tasks"], force=True)

celery_app.conf.beat_schedule = {
    "send_email_report": {
        "task": "src.tasks.send_email_report",
        "schedule": crontab(hour=10, minute=0),
    },
}
