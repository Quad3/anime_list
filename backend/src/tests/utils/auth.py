from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from .utils import random_lower_string


async def create_random_user(session: AsyncSession) -> User:
    db_obj = User(
        username=random_lower_string(),
        password=random_lower_string(),
    )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj
