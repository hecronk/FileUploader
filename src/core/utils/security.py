from argon2 import PasswordHasher, exceptions
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt

from src.core.settings.settings import settings


ph = PasswordHasher(
    time_cost=2,
    memory_cost=64,
    parallelism=4
)

async def get_password_hash(key: str) -> str:
    return ph.hash(key)

async def verify_password(key: str, stored_hash: str) -> bool:
    try:
        return ph.verify(stored_hash, key)
    except VerifyMismatchError:
        return False

async def needs_rehash(stored_hash: str):
    return ph.check_needs_rehash(stored_hash)

async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

async def decode_access_token(token: str):
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
