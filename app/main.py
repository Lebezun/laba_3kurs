from fastapi import FastAPI
from app.api.users import router as users_router

app = FastAPI(title="Lab 3 - FastAPI CRUD")

# Підключаємо наш роутер юзерів
app.include_router(users_router, prefix="/users", tags=["Users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Lab 3"}