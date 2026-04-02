from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Створюємо асинхронний двигун
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Фабрика сесій (викладач оцінить)
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# Залежність для отримання сесії в роутерах
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session