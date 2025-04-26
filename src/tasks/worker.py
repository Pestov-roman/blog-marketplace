from celery import Celery

# Инициализация Celery
celery = Celery(
    "blog_marketplace", broker="amqp://guest:guest@rabbitmq:5672//", backend="rpc://"
)

celery.autodiscover_tasks(["src.tasks"])


@celery.task(name="health_check")
def health_check():
    return "Celery is working fine!"
