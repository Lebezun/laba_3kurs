import pytest
import asyncio
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import declarative_base

from app.main import app
from app.db.session import get_db, Base

TEST_DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/test_db"


# 1. Цикл для ВСІХ тестів
@pytest.fixture(scope="session")
def event_loop():
    """Створює event loop для всієї сесії тестів"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


# 2. Двигун з NullPool
@pytest_asyncio.fixture(scope="session")
async def engine():
    """Створює асинхронний двигун для тестової БД"""
    test_engine = create_async_engine(
        TEST_DATABASE_URL, 
        echo=False, 
        poolclass=NullPool
    )
    yield test_engine
    await test_engine.dispose()


# 3. Підготовка БД перед кожним тестом
@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db(engine):
    """Очищує БД перед кожним тестом та перехоплює залежність get_db"""
    TestingSessionLocal = async_sessionmaker(
        bind=engine, 
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    
    # Створюємо/очищуємо схему
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    app.dependency_overrides.clear()


# 4. HTTP клієнт для тестів
@pytest_asyncio.fixture(scope="function")
async def client():
    """Створює асинхронний HTTP клієнт для тестування API"""
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, 
        base_url="http://test", 
        follow_redirects=True
    ) as ac:
        yield ac