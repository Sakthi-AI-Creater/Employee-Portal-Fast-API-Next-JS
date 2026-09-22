from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    verify_password,
)
from app.modules.users import repository
from app.modules.users.model import User


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User:

    user = repository.get_user_by_email(
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


def login_user(
    db: Session,
    email: str,
    password: str,
) -> str:

    user = authenticate_user(
        db,
        email,
        password,
    )

    return create_access_token(
        user.id
    )