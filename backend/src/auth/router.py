from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from config import settings
from .deps import SessionDep
from .schemas import UserRead, UserCreate, UserRegister, Token
from .service import get_user_by_email, create_user, authenticate
from security import create_access_token
from utils import send_email, generate_new_account_email

router = APIRouter(
    tags=["Auth"],
    prefix="/users",
)


@router.post("/access-token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    user = await authenticate(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return Token(
        access_token=create_access_token(
            user.uuid, expires_delta=access_token_expires
        )
    )


@router.post("/signup", response_model=UserRead)
async def register_user(session: SessionDep, user_register: UserRegister):
    db_user = await get_user_by_email(session, user_register.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system",
        )

    user_create = UserCreate(
        **user_register.model_dump(),
        is_active=True,
        is_superuser=False,
    )
    user = await create_user(session, user_create)
    email_data = generate_new_account_email(
        email=user_create.email,
        password=user_create.password,
    )
    send_email(
        email_to=user_create.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return user
