from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from security import verify_password, get_password_hash
from .models import User
from .schemas import UserCreate


async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
    db_obj = User(
        username=user_create.username,
        password=get_password_hash(user_create.password)
    )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result = await session.scalars(stmt)
    return result.first()


async def authenticate(session: AsyncSession, username: str, password: str) -> User | None:
    db_user = await get_user_by_username(session, username)
    if not db_user:
        return None
    if not verify_password(password, db_user.password):
        return None
    return db_user
