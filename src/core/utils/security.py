from argon2 import PasswordHasher, exceptions
from argon2.exceptions import VerifyMismatchError

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
