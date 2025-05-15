from celery import shared_task

from src.utils.email import send_email


@shared_task(  # type: ignore
    name="email.send_registration",
    autoretry_for=(Exception,),
    retry_kwargs={'max_retries': 3, 'countdown': 2}
)
def send_registration_email(to: str) -> None:
    import asyncio

    html = (
        "<h3>Добро пожаловать!</h3>"
        "<p>Вы успешно зарегистрированы в блоге маркетплейса.</p>"
    )
    asyncio.run(send_email("Регистрация успешна", html, [to]))
