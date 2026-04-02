from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Правильні імпорти з твоїх файлів
from app.db.session import get_db
from app.schemas.product import CategoryCreate, CategoryResponse, ProductCreate, ProductResponse
from app.crud import crud_product

# Створюємо сам роутер (це, мабуть, теж загубилося)
router = APIRouter()

@router.post("/categories/", response_model=CategoryResponse)
async def create_category_endpoint(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await crud_product.create_category(db=db, category=category)

@router.post("/products/", response_model=ProductResponse)
async def create_product_endpoint(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await crud_product.create_product(db=db, product=product)

@router.get("/products/", response_model=list[ProductResponse])
async def read_products(db: AsyncSession = Depends(get_db)):
    return await crud_product.get_products(db)