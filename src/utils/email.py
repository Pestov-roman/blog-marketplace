from email.message import EmailMessage

import aiosmtplib

from src.settings import settings


async def send_email(
    subject: str,
    html: str,
    to: list[str],
) -> None:
    message = EmailMessage()
    message["From"] = settings.smtp_from
    message["To"] = ", ".join(to)
    message["Subject"] = subject
    message.set_content(html, subtype="html")

    await aiosmtplib.send(
        message,
        hostname=settings.smtp_host,
        port=settings.smtp_port,
        username=settings.smtp_user,
        password=settings.smtp_password,
    )
