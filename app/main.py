from fastapi import FastAPI
from app.api.users import router as users_router
from app.api.products import router as products_router

app = FastAPI(title="Lab 4 API")

# Підключаємо наш роутер юзерів
app.include_router(users_router, prefix="/users", tags=["Users"])

app.include_router(products_router, prefix="/store", tags=["store"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Lab 3"}