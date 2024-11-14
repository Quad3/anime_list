import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder

from .utils.utils import random_lower_string, random_email
from auth.schemas import UserCreate
from auth.service import create_user, authenticate
from auth.models import User


@pytest.mark.anyio
async def test_create_user(test_db: AsyncSession):
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = await create_user(session=test_db, user_create=user_in)
    assert user.email == email
    assert hasattr(user, "password")


@pytest.mark.anyio
async def test_check_if_user_is_active(test_db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = await create_user(session=test_db, user_create=user_in)
    assert user.is_active is True


@pytest.mark.anyio
async def test_check_if_user_is_superuser(test_db: AsyncSession):
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    user = await create_user(session=test_db, user_create=user_in)
    assert user.is_superuser is True


@pytest.mark.anyio
async def test_check_if_user_is_superuser_normal_user(test_db: AsyncSession):
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = await create_user(session=test_db, user_create=user_in)
    assert user.is_superuser is False


@pytest.mark.anyio
async def test_authenticate_user(test_db: AsyncSession):
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = await create_user(session=test_db, user_create=user_in)
    authenticated_user = await authenticate(test_db, email, password)
    assert authenticated_user
    assert user.email == authenticated_user.email


@pytest.mark.anyio
async def test_not_authenticate_user(test_db: AsyncSession):
    email = random_email()
    password = random_lower_string()
    user = await authenticate(test_db, email, password)
    assert user is None


@pytest.mark.anyio
async def test_get_user(test_db: AsyncSession):
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = await create_user(session=test_db, user_create=user_in)
    user2 = await test_db.get(User, user.uuid)
    assert user2
    assert user.email == user2.email
    assert jsonable_encoder(user) == jsonable_encoder(user2)
