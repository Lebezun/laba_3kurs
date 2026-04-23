from fastapi import Depends, HTTPException, status, Request
from jose import jwt, JWTError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.database import User
from app.core.config import settings


async def create_user(db: AsyncSession, user):
    """Створює нового користувача в БД"""
    db_user = User(
        username=user.username, 
        email=user.email, 
        password=user.password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def authenticate_user(db: AsyncSession, username: str, password: str):
    """Аутентифікує користувача за іменем та паролем"""
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalars().first()
    if not user:
        return False
    # Порівняння пароля (для лаби просто текстовий)
    if password != user.password: 
        return False
    return user


async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)):
    """Отримує поточного користувача з JWT токена"""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        token = token.split(" ")[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except (JWTError, IndexError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


async def get_user_by_email(db: AsyncSession, email: str):
    """Отримує користувача за email"""
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def get_user_by_id(db: AsyncSession, user_id: int):
    """Отримує користувача за ID"""
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str):
    """Отримує користувача за іменем"""
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()


async def get_all_users(db: AsyncSession):
    """Отримує всіх користувачів"""
    result = await db.execute(select(User))
    return result.scalars().all()
