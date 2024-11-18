from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from auth.schemas import UserCreate
from auth.service import create_user
from .utils import random_lower_string, random_email


async def create_random_user(session: AsyncSession) -> User:
    db_obj = User(
        email=random_email(),
        password=random_lower_string(),
    )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def user_token_headers(
        async_client: AsyncClient,
        test_db: AsyncSession,
) -> dict[str, str]:
    credentials = {
        "email": "test@test.com",
        "password": "test_password",
    }
    user_create = UserCreate(**credentials)
    await create_user(test_db, user_create)
    return await get_user_token_headers(async_client, user_create)


async def get_user_token_headers(
        async_client: AsyncClient,
        login_data: UserCreate,
) -> dict[str, str]:
    r = await async_client.post(
        "users/access-token",
        data={"username": login_data.email, "password": login_data.password},
    )
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
