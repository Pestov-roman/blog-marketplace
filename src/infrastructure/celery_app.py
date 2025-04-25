from celery import Celery
from celery.schedules import crontab

from src.settings import settings

celery_app = Celery(
    "blog-marketplace",
    broker=settings.rabbitmq_dsn,
    backend="rpc://",
)

celery_app.autodiscover_tasks(["src.tasks"], force=True)

celery_app.conf.beat_schedule = {
    "send_email_report": {
        "task": "src.tasks.send_email_report",
        "schedule": crontab(hour=10, minute=0),
    },
}
