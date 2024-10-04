from pydantic import BaseModel, ConfigDict, Field
from pydantic.types import UUID4


class UserBase(BaseModel):
    username: str = Field(max_length=128)
    is_active: bool = True
    is_superuser: bool = False


class UserRegister(BaseModel):
    username: str = Field(max_length=128)
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
