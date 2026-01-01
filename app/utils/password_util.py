import secrets
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    if not password or len(password) < 8:
      raise ValueError("Password must be at least 8 characters long")

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def generate_secret_key(length: int = 32) -> str:
    return secrets.token_urlsafe(length)
