from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from config import settings


Base = declarative_base()

engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI), future=True, echo=True)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_db():
    session: AsyncSession = async_session()
    try:
        yield session
    finally:
        await session.close()
