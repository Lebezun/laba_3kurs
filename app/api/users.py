from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserResponse
from app.db.session import get_db
from app.crud import crud_user

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Тепер ми зберігаємо не в словник, а в Postgres!
    return await crud_user.create_user(db=db, user=user)

@router.get("/", response_model=list[UserResponse])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    users = await crud_user.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user