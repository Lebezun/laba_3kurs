from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import jwt

from app.db.session import get_db
from app.models.database import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings

router = APIRouter()

# ==========================================
# ФУНКЦІЯ-ОХОРОНЕЦЬ (Дістає токен з кукі)
# ==========================================
async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)):
    # Шукаємо куку з назвою access_token
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated (No cookie)")
    
    try:
        # Відрізаємо слово "Bearer " від токена, якщо воно є
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
            
        # Розшифровуємо нашим секретним ключем
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
            
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    # Шукаємо юзера в базі
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user


# ==========================================
# 1. РЕЄСТРАЦІЯ (Зберігаємо хеш замість пароля)
# ==========================================
@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Перевіряємо, чи не зайнятий емейл
    result = await db.execute(select(User).filter(User.email == user.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Солимо і хешуємо пароль!
    hashed_pwd = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, password=hashed_pwd)
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


# ==========================================
# 2. ЛОГІН (Видаємо JWT і кладемо в Cookie)
# ==========================================
@router.post("/login")
async def login(response: Response, user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Шукаємо юзера
    result = await db.execute(select(User).filter(User.email == user_data.email))
    user = result.scalars().first()

    # Перевіряємо, чи співпадає пароль з хешем у базі
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    # Генеруємо токен, записуючи туди емейл юзера
    access_token = create_access_token(data={"sub": user.email})

    # Кладемо токен у безпечну HttpOnly куку!
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,  # Захист від крадіжки токена через JS
        max_age=1800,   # 30 хвилин
        samesite="lax"
    )
    return {"message": "Login successful. Cookie set!"}


# ==========================================
# 3. ЗАХИЩЕНА РУЧКА (Вимагає аутентифікованого юзера)
# ==========================================
@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    # Ця ручка спрацює ТІЛЬКИ якщо в запиті є правильна кука
    return current_user


# ==========================================
# 4. ЛОГАУТ (Очищає куку)
# ==========================================
@router.post("/logout")
async def logout(response: Response):
    # Видаляємо куку, щоб юзер вийшов з акаунту
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}