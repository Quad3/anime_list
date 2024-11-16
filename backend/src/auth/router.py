from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm

from config import settings
from .deps import SessionDep
from .schemas import UserRead, UserCreate, UserRegister, Token, Message, NewPassword
from .service import get_user_by_email, create_user, authenticate, password_reset
from security import create_access_token
from utils import (
    send_email,
    generate_new_account_email,
    generate_password_reset_token,
    generate_reset_password_email,
    verify_password_reset_token,
    generate_reset_password_success_email,
)

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
async def register_user(session: SessionDep, user_register: UserRegister, background_tasks: BackgroundTasks):
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
    email_data = await generate_new_account_email(
        email=user_create.email,
        password=user_create.password,
    )
    background_tasks.add_task(
        send_email,
        email_to=user_create.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return user


@router.post("/password-recovery/{email}")
async def recover_password(email: str, session: SessionDep, background_tasks: BackgroundTasks) -> Message:
    user = await get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this email does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    email_data = await generate_reset_password_email(
        email=email, token=password_reset_token
    )
    background_tasks.add_task(
        send_email,
        email_to=user.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Password recovery email sent")


@router.post("/reset-password")
async def reset_password(session: SessionDep, body: NewPassword, background_tasks: BackgroundTasks) -> Message:
    email = verify_password_reset_token(token=body.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = await get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    await password_reset(session, user, body.new_password)
    email_data = await generate_reset_password_success_email(email=email, new_password=body.new_password)
    background_tasks.add_task(
        send_email,
        email_to=user.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Password updated successfully")
