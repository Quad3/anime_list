from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

from security import verify_password, get_password_hash
from .models import User
from .schemas import UserCreate


async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
    db_obj = User(
        email=user_create.email,
        password=get_password_hash(user_create.password),
        is_active=user_create.is_active,
        is_superuser=user_create.is_superuser,
    )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def get_user_by_email(session: AsyncSession, email: EmailStr) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await session.scalars(stmt)
    return result.first()


async def authenticate(session: AsyncSession, email: EmailStr, password: str) -> User | None:
    db_user = await get_user_by_email(session, email)
    if not db_user:
        return None
    if not verify_password(password, db_user.password):
        return None
    return db_user


async def password_reset(session: AsyncSession, user: User, new_password: str):
    user.password = get_password_hash(password=new_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
