from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app.core.config import settings

from app.core.security import (
    create_access_token,
    generate_refresh_token,
    hash_refresh_token,
    verify_password,
    verify_refresh_token,
)
from app.modules.auth import repository
from app.modules.auth.model import RefreshToken
from app.modules.users import repository as user_repository
from app.modules.users.model import User


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User:

    user = user_repository.get_user_by_email(
        db,
        email,
    )

    if not user:
        raise ValueError("Invalid email or password")

    if not user.is_active:
        raise ValueError("User account is inactive")

    if not verify_password(
        password,
        user.password_hash,
    ):
        raise ValueError("Invalid email or password")

    return user

def create_refresh_token_for_user(
    db: Session,
    user_id: int,
) -> str:

    token_id = generate_refresh_token_id()

    token_secret = generate_refresh_token()

    token_hash = hash_refresh_token(
        token_secret
    )

    expires_at = (
        datetime.now(timezone.utc)
        + timedelta(
            days=settings.jwt_refresh_token_expire_days
        )
    )

    refresh_token_record = RefreshToken(
        user_id=user_id,
        token_id=token_id,
        token_hash=token_hash,
        expires_at=expires_at,
    )

    repository.create_refresh_token(
        db,
        refresh_token_record,
    )

    return f"{token_id}.{token_secret}"


def refresh_user_session(
    db: Session,
    raw_refresh_token: str,
) -> tuple[str, str]:

    try:
        token_id, token_secret = (
            raw_refresh_token.split(".", 1)
        )
    except ValueError:
        raise ValueError("Invalid refresh token")

    refresh_token_record = repository.get_refresh_token(
        db,
        token_id,
    )

    if not refresh_token_record:
        raise ValueError("Invalid refresh token")

    if refresh_token_record.revoked_at is not None:
        raise ValueError("Refresh token has been revoked")

    if refresh_token_record.expires_at <= datetime.now(
        timezone.utc
    ):
        raise ValueError("Refresh token has expired")

    if not verify_refresh_token(
        token_secret,
        refresh_token_record.token_hash,
    ):
        raise ValueError("Invalid refresh token")

    user = user_repository.get_user_by_id(
        db,
        refresh_token_record.user_id,
    )

    if not user:
        raise ValueError("User not found")

    if not user.is_active:
        raise ValueError("User account is inactive")

    # Revoke old refresh token
    repository.revoke_refresh_token(
        db,
        refresh_token_record,
    )

    # Create new access token
    new_access_token = create_access_token(
        user.id
    )

    # Create new refresh token
    new_refresh_token = create_refresh_token_for_user(
        db,
        user.id,
    )

    return (
        new_access_token,
        new_refresh_token,
    )


def login_user(
    db: Session,
    email: str,
    password: str,
) -> tuple[str, str]:

    # Authenticate user
    user = authenticate_user(
        db,
        email,
        password,
    )

    # Create short-lived access token
    access_token = create_access_token(
        user.id
    )

    # Create long-lived refresh token
    refresh_token = create_refresh_token_for_user(
        db,
        user.id,
    )

    return access_token, refresh_token