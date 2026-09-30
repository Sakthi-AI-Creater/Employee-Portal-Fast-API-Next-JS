from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.auth.model import RefreshToken


def create_refresh_token(
    db: Session,
    refresh_token: RefreshToken,
) -> RefreshToken:

    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)

    return refresh_token


def get_refresh_token(
    db: Session,
    token_id: str,
) -> RefreshToken | None:

    statement = select(RefreshToken).where(
        RefreshToken.token_id == token_id
    )

    return db.scalar(statement)


def revoke_refresh_token(
    db: Session,
    refresh_token: RefreshToken,
) -> RefreshToken:

    refresh_token.revoked_at = datetime.utcnow()

    db.commit()
    db.refresh(refresh_token)

    return refresh_token