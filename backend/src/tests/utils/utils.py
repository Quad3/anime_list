import random
import string

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from auth.schemas import UserCreate
from auth.service import create_user


async def get_user_token_headers(
        async_client: AsyncClient,
        login_data: UserCreate,
) -> dict[str, str]:
    r = await async_client.post("users/access-token", data=login_data.model_dump())
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


async def user_token_headers(
        async_client: AsyncClient,
        test_db: AsyncSession,
) -> dict[str, str]:
    credentials = {
        "username": "test_username",
        "password": "test_password",
    }
    user_create = UserCreate(**credentials)
    await create_user(test_db, user_create)
    return await get_user_token_headers(async_client, user_create)


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))
