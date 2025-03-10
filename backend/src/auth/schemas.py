from pydantic import BaseModel, ConfigDict, Field, EmailStr
from pydantic.types import UUID4


class UserBase(BaseModel):
    email: EmailStr = Field(max_length=128)
    is_active: bool = True
    is_superuser: bool = False


class UserRegister(BaseModel):
    email: EmailStr = Field(max_length=128)
    password: str = Field(min_length=8, max_length=40)


class UserRead(UserBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    uuid: UUID4


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str | None = None


class NewPassword(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


class Message(BaseModel):
    message: str
