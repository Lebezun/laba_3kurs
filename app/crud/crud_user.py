from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.database import User
from app.schemas.user import UserCreate

async def get_user(db: AsyncSession, user_id: int):
    # Асинхронний запит на пошук юзера за ID
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    # Отримання списку юзерів
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

async def create_user(db: AsyncSession, user: UserCreate):
    # Створення нового юзера в реальній БД
    db_user = User(username=user.username, email=user.email, password=user.password)
    db.add(db_user)
    await db.commit() # Зберігаємо зміни
    await db.refresh(db_user) # Оновлюємо об'єкт, щоб отримати згенерований ID
    return db_user