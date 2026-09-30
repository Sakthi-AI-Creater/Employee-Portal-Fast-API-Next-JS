from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
from app.core.config import settings
import secrets


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return password_hash.verify(
        plain_password,
        hashed_password,
    )

def create_access_token(
    user_id: int,
) -> str:

    expires_at = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=settings.jwt_access_token_expire_minutes
        )
    )

    payload = {
        "sub": str(user_id),
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

def generate_refresh_token() -> str:
    return secrets.token_urlsafe(64)

def generate_refresh_token_id() -> str:
    return secrets.token_urlsafe(32)

def hash_refresh_token(token: str) -> str:
    return password_hash.hash(token)

def verify_refresh_token(
    token: str,
    token_hash: str,
) -> bool:
    return password_hash.verify(
        token,
        token_hash,
    )