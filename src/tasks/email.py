from celery import shared_task

from src.utils.email import send_email


@shared_task(name="email.send_registration")  # type: ignore[misc]
def send_registration_email(to: str) -> None:
    import asyncio

    html = (
        "<h3>Добро пожаловать!</h3>"
        "<p>Вы успешно зарегистрированы в блоге маркетплейса.</p>"
    )
    asyncio.run(send_email("Регистрация успешна", html, [to]))
