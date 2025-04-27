import pytest
from celery.result import EagerResult

from src.infrastructure.celery_app import celery_app


@pytest.fixture(autouse=True, scope="session")
def _eager():
    celery_app.conf.task_always_eager = True
    yield
    celery_app.conf.task_always_eager = False


def test_health_check_task():
    from src.tasks.worker import health_check

    res: EagerResult = health_check.delay()
    assert res.successful()
    assert res.result == "OK"
