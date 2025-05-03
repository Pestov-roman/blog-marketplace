from typing import cast

from passlib.hash import bcrypt


def hash_password(password: str) -> str:
    return cast(str, bcrypt.hash(password))


def verify_password(password: str, hashed_password: str) -> bool:
    return cast(bool, bcrypt.verify(password, hashed_password))
