from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.schemas.user import UserCreate, UserResponse
from app.db.session import get_db
from app.crud import crud_user
from app.core.security import create_access_token

router = APIRouter()

# 1. РЕЄСТРАЦІЯ
@router.post("/register", response_model=UserResponse)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud_user.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    try:
        return await crud_user.create_user(db=db, user=user_in)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username already registered")

# 2. ЛОГІН (Для отримання токена)
@router.post("/login")
async def login(
    response: Response, 
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    user = await crud_user.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password"
        )
    
    # Створюємо JWT токен
    access_token = create_access_token(data={"sub": user.username})
    
    # Записуємо токен у Куки
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    
    return {"access_token": access_token, "token_type": "bearer"}

# 3. ПРОФІЛЬ (Ручка /me)
@router.get("/me", response_model=UserResponse)
async def read_user_me(
    current_user = Depends(crud_user.get_current_user)
):
    return current_user
