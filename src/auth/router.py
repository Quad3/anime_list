from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from .deps import SessionDep
from .schemas import UserRead, UserCreate, Token
from .service import get_user_by_username, create_user, authenticate
from security import create_access_token


router = APIRouter(
    tags=["Anime"],
    prefix="/users",
)


@router.post("/access-token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    user = await authenticate(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    return Token(
        access_token=create_access_token(
            user.uuid, expires_delta=access_token_expires
        )
    )


@router.post("/signup", response_model=UserRead)
async def register_user(session: SessionDep, user_create: UserCreate):
    db_user = await get_user_by_username(session, user_create.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system",
        )
    user = await create_user(session, user_create)
    return user
