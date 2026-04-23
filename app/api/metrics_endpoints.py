"""
API endpoints для оновлення кастомних метрик
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from app.db.session import get_db
from app.models.database import User, Product, Category
from app.core.metrics import (
    total_users_count,
    total_products_count,
    total_categories_count,
    total_products_price,
    products_price_by_category,
    average_product_price,
    max_product_price,
    min_product_price
)

router = APIRouter()

@router.post("/update-metrics")
async def update_metrics(db: AsyncSession = Depends(get_db)):
    """
    Ручка для оновлення кастомних метрик з БД.
    Зазвичай викликається periodically або після важливих операцій.
    """
    
    # ========== Користувачі ==========
    users_result = await db.execute(select(func.count(User.id)))
    users_count = users_result.scalar()
    total_users_count.set(users_count or 0)
    
    # ========== Товари ==========
    products_result = await db.execute(select(func.count(Product.id)))
    products_count = products_result.scalar()
    total_products_count.set(products_count or 0)
    
    # ========== Категорії ==========
    categories_result = await db.execute(select(func.count(Category.id)))
    categories_count = categories_result.scalar()
    total_categories_count.set(categories_count or 0)
    
    # ========== КАСТОМНА МЕТРИКА 1: Сумарна ціна всіх товарів ==========
    total_price_result = await db.execute(
        select(func.sum(Product.price))
    )
    total_price = total_price_result.scalar() or 0
    total_products_price.labels(currency='UAH').set(float(total_price))
    
    # ========== КАСТОМНА МЕТРИКА 2: Ціна товарів по категоріям ==========
    # Отримуємо всі категорії з їх товарами
    categories_with_prices = await db.execute(
        select(
            Category.name,
            func.sum(Product.price).label('total_price')
        ).join(Product, Category.id == Product.category_id, isouter=True)
        .group_by(Category.id, Category.name)
    )
    
    for category_name, category_total_price in categories_with_prices:
        price = float(category_total_price or 0)
        products_price_by_category.labels(category_name=category_name).set(price)
    
    # ========== Статистика цін товарів ==========
    if products_count and products_count > 0:
        # Середня ціна
        avg_price_result = await db.execute(
            select(func.avg(Product.price))
        )
        avg_price = avg_price_result.scalar() or 0
        average_product_price.set(float(avg_price))
        
        # Найдорожчий товар
        max_price_result = await db.execute(
            select(func.max(Product.price))
        )
        max_price = max_price_result.scalar() or 0
        max_product_price.set(float(max_price))
        
        # Найдешевший товар
        min_price_result = await db.execute(
            select(func.min(Product.price))
        )
        min_price = min_price_result.scalar() or 0
        min_product_price.set(float(min_price))
    
    return {
        "status": "success",
        "metrics": {
            "total_users": users_count or 0,
            "total_products": products_count or 0,
            "total_categories": categories_count or 0,
            "total_products_price_uah": float(total_price),
            "average_product_price_uah": float(avg_price if products_count else 0),
            "max_product_price_uah": float(max_price if products_count else 0),
            "min_product_price_uah": float(min_price if products_count else 0),
        }
    }

@router.get("/metrics-info")
async def get_metrics_info(db: AsyncSession = Depends(get_db)):
    """
    Отримати поточні значення кастомних метрик без оновлення
    """
    await update_metrics(db)
    
    # Отримуємо всі категорії
    categories_result = await db.execute(select(Category))
    categories = categories_result.scalars().all()
    
    categories_prices = {}
    for cat in categories:
        price_result = await db.execute(
            select(func.sum(Product.price)).where(Product.category_id == cat.id)
        )
        price = price_result.scalar() or 0
        categories_prices[cat.name] = float(price)
    
    return {
        "status": "success",
        "data": {
            "categories_prices": categories_prices
        }
    }
