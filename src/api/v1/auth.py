from fastapi import APIRouter, Depends, Response, status

from src.application.ports.uow import UnitOfWork
from src.auth.jwt import create_access_token
from src.auth.password import hash_password
from src.auth.schemas import LoginIn, TokenOut
from src.domain.models import User
from src.infrastructure.uow.sqlalchemy import get_uow
from src.tasks.email import send_registration_email

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=TokenOut)
async def register(
    dto: LoginIn,
    response: Response,
    uow: UnitOfWork = Depends(get_uow),
):
    user = User.create(dto.email, hash_password(dto.password))
    await uow.users.add(user)
    await uow.commit()
    send_registration_email.delay(user.email)
    token = create_access_token(user.id)
    response.set_cookie("access_token", token, httponly=True)
    return {"access_token": token}


@router.post("/login", response_model=TokenOut)
async def login(
    dto: LoginIn,
    response: Response,
    uow: UnitOfWork = Depends(get_uow),
):
    user = await uow.users.by_email(dto.email)
    token = create_access_token(user.id)
    response.set_cookie("access_token", token, httponly=True)
    return {"access_token": token}
