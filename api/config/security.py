from jose import jwt  # type:ignore
from passlib.context import CryptContext  # type:ignore

from datetime import datetime, timedelta
from typing import Union, Any, Optional

from .dynaconf import settings

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = settings.ALGORITHM
JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_REFRESH_SECRET_KEY = settings.JWT_REFRESH_SECRET_KEY

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: str, expires_delta: Optional[int]) -> str:
    expires_delta = _create_expires_delta(
        expires_delta, ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expires_delta, "sub": subject}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)

    return encoded_jwt


def create_refresh_token(subject: str, expires_delta: Optional[int]) -> str:
    expires_delta = _create_expires_delta(
        expires_delta, REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expires_delta, "sub": subject}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)

    return encoded_jwt


def _create_expires_delta(expires_delta: Optional[int], token_time: int):
    if expires_delta:
        expires_datetime = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expires_datetime = datetime.utcnow() + timedelta(minutes=token_time)

    return expires_datetime
