from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    employee_id: str
    name: str
    email: EmailStr
    password: str
    role: str = "employee"


class UserResponse(BaseModel):
    id: int
    employee_id: str
    name: str
    email: EmailStr
    role: str
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )