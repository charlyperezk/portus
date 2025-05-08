import os
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

PEPPER = os.getenv("PASSWORD_PEPPER", "SECRET") # Delete default value in production

ph = PasswordHasher(
    time_cost=2, 
    memory_cost=102400,
    parallelism=8,
)

def hash_password(password: str) -> str:
    password_with_pepper = password.encode() + PEPPER.encode()
    return ph.hash(password_with_pepper)

def verify_password(password: str, hash: str) -> bool:
    password_with_pepper = password.encode() + PEPPER.encode()
    try:
        return ph.verify(hash, password_with_pepper)
    except VerifyMismatchError:
        return False