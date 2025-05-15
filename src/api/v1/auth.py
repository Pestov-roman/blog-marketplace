import asyncio
import logging
import socket

from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.application.ports.uow import UnitOfWork
from src.auth.jwt import create_access_token
from src.auth.password import verify_password
from src.auth.roles import Role
from src.auth.schemas import LoginIn, TokenOut
from src.domain.models import User
from src.infrastructure.di import get_uow
from src.settings import settings
from src.tasks.email import send_registration_email

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/health/rabbitmq")
async def rabbitmq_health():
    try:
        host = settings.rabbitmq_host
        port = settings.rabbitmq_port
        with socket.create_connection((host, port), timeout=5):
            return {"status": "ok"}
    except Exception as e:
        logging.error(f"RabbitMQ healthcheck failed: {e}")
        return {"status": "fail", "error": str(e)}


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=TokenOut)
async def register(
    dto: LoginIn,
    response: Response,
    uow: UnitOfWork = Depends(get_uow),
) -> TokenOut:
    existing_user = await uow.users.by_email(dto.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже существует"
        )
    role = dto.role if dto.role else Role.READER
    user = User.create(dto.email, dto.password, role)
    await uow.users.add(user)
    await uow.commit()
    try:
        send_registration_email.delay(user.email)
    except Exception as e:
        logging.error(f"Failed to send registration email: {e}")
    token = create_access_token(str(user.id), user.role)
    response.set_cookie("access_token", token, httponly=True)
    return TokenOut(access_token=token, token_type="bearer")


@router.post(
    "/register/author", 
    status_code=status.HTTP_201_CREATED, 
    response_model=TokenOut
)
async def register_author(
    dto: LoginIn,
    response: Response,
    uow: UnitOfWork = Depends(get_uow),
) -> TokenOut:
    existing_user = await uow.users.by_email(dto.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже существует"
        )
    user = User.create(dto.email, dto.password, Role.AUTHOR)
    await uow.users.add(user)
    await uow.commit()
    try:
        send_registration_email.delay(user.email)
    except Exception as e:
        logging.error(f"Failed to send registration email: {e}")
    token = create_access_token(str(user.id), user.role)
    response.set_cookie("access_token", token, httponly=True)
    return TokenOut(access_token=token, token_type="bearer")


@router.post("/login", response_model=TokenOut)
async def login(
    dto: LoginIn,
    response: Response,
    uow: UnitOfWork = Depends(get_uow),
) -> TokenOut:
    user = await uow.users.by_email(dto.email)
    if not user or not verify_password(dto.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    token = create_access_token(str(user.id), user.role)
    response.set_cookie("access_token", token, httponly=True)
    return TokenOut(access_token=token, token_type="bearer")
