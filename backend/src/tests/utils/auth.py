from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
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
