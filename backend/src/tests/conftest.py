import asyncio
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.sql import text
from asyncpg import Connection
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory

from main import app
from config import settings
from database import Base, get_db


test_engine = create_async_engine(
    str(settings.SQLALCHEMY_TEST_DATABASE_URI),
    future=True,
    echo=True,
)


@pytest.fixture(scope="session")
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def run_migrations(connection: Connection):
    config = Config("alembic.ini")
    config.set_main_option("script_location", "src/migrations")
    config.set_main_option("sqlalchemy.url", str(settings.SQLALCHEMY_TEST_DATABASE_URI))
    script = ScriptDirectory.from_config(config)

    def upgrade(rev, context):
        return script._upgrade_revs("head", rev)

    context = MigrationContext.configure(connection, opts={"target_metadata": Base.metadata, "fn": upgrade})

    with context.begin_transaction():
        with Operations.context(context):
            context.run_migrations()


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    async with test_engine.connect() as connection:
        await connection.run_sync(run_migrations)

    yield

    await test_engine.dispose()


@pytest.fixture(scope="function")
async def test_db():
    test_session = async_sessionmaker(
        expire_on_commit=False,
        autoflush=False,
        bind=test_engine,
        class_=AsyncSession
    )

    async with test_session() as session:
        await session.begin()

        yield session

        await session.rollback()

        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(text(f"TRUNCATE {table.name} CASCADE;"))
            await session.commit()


@pytest.fixture()
async def test_app(test_db):
    """Injecting test database as dependency in app for tests."""
    async def test_get_database():
        yield test_db

    app.dependency_overrides[get_db] = test_get_database

    return app


@pytest.fixture()
async def async_client(test_app) -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=f"http://{settings.DOMAIN}{settings.API_V1_STR}"
    ) as ac:
        yield ac
