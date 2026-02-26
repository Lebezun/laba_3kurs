from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter()

# Наша "база даних" - звичайний словник
fake_db = {}
current_id = 1


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    global current_id
    new_user = {"id": current_id, **user.model_dump()}
    fake_db[current_id] = new_user
    current_id += 1
    return new_user


@router.get("/", response_model=list[UserResponse])
def get_all_users():
    return list(fake_db.values())


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    return fake_db[user_id]


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")

    stored_data = fake_db[user_id]
    update_data = user.model_dump(exclude_unset=True)  # Оновлюємо тільки те, що передали
    updated_user = {**stored_data, **update_data}
    fake_db[user_id] = updated_user
    return updated_user


@router.delete("/{user_id}")
def delete_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    del fake_db[user_id]
    return {"message": "User deleted successfully"}