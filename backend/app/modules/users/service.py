from sqlalchemy.orm import Session

from app.modules.users import repository
from app.modules.users.model import User
from app.modules.users.schema import UserCreate



def create_user(
    db: Session,
    user_data: UserCreate,
) -> User:

    existing_email = repository.get_user_by_email(
        db,
        user_data.email,
    )

    if existing_email:
        raise ValueError("Email already registered")

    existing_employee = repository.get_user_by_employee_id(
        db,
        user_data.employee_id,
    )

    if existing_employee:
        raise ValueError("Employee ID already registered")

    user = User(
        employee_id=user_data.employee_id,
        name=user_data.name,
        email=user_data.email,
        password_hash=user_data.password,
        role=user_data.role,
    )

    return repository.create_user(
        db,
        user,
    )