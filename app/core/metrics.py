from prometheus_client import Counter, Histogram, Gauge, Info

# --- Стандартні HTTP метрики ---
http_requests_total = Counter(
    "http_requests_total", 
    "Total number of HTTP requests", 
    ["method", "endpoint", "status"]
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds", 
    "HTTP request duration in seconds", 
    ["method", "endpoint"],
    buckets=(0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0)
)

http_errors_total = Counter(
    "http_errors_total", 
    "Total number of HTTP errors", 
    ["method", "endpoint", "status_code"]
)

# --- Метрики продуктів ---
products_created_total = Counter("products_created_total", "Total number of created products")
products_deleted_total = Counter("products_deleted_total", "Total number of deleted products")
products_updated_total = Counter("products_updated_total", "Total number of updated products")
categories_created_total = Counter("categories_created_total", "Total number of created categories")

# --- Метрики цін (ДЛЯ ЛАБИ) ---
total_purchases_price = Gauge("total_purchases_price", "Сумарна ціна всіх покупок")
average_product_price = Gauge("average_product_price", "Середня ціна продукту")
products_in_stock = Gauge("products_in_stock", "Кількість продуктів в каталозі")
categories_count = Gauge("categories_count", "Кількість категорій")

# === ДОДАНО: ВІДСУТНІ МЕТРИКИ ===
total_users_count = Gauge("total_users_count", "Загальна кількість користувачів")
total_products_count = Gauge("total_products_count", "Загальна кількість товарів")
total_categories_count = Gauge("total_categories_count", "Загальна кількість категорій")
total_products_price = Gauge("total_products_price", "Сумарна ціна всіх товарів", ["currency"])
products_price_by_category = Gauge("products_price_by_category", "Ціна товарів по категоріям", ["category_name"])
max_product_price = Gauge("max_product_price", "Максимальна ціна товару")
min_product_price = Gauge("min_product_price", "Мінімальна ціна товару")

# --- Інформаційна метрика ---
app_info = Info("app_info", "Application information")


# --- Функції для оновлення метрик ---
async def update_product_metrics(db):
    """Оновлює метрики продуктів на основі даних з БД"""
    try:
        from sqlalchemy.future import select
        from sqlalchemy import func
        from app.models.database import Product, Category
        
        # Загальна кількість продуктів
        result = await db.execute(select(func.count(Product.id)))
        product_count = result.scalar() or 0
        products_in_stock.set(product_count)
        
        # Сумарна ціна всіх продуктів
        result = await db.execute(select(func.sum(Product.price)))
        total_price = result.scalar() or 0
        total_purchases_price.set(float(total_price))
        
        # Середня ціна продукту
        result = await db.execute(select(func.avg(Product.price)))
        avg_price = result.scalar() or 0
        average_product_price.set(float(avg_price))
        
        # Кількість категорій
        result = await db.execute(select(func.count(Category.id)))
        category_count = result.scalar() or 0
        categories_count.set(category_count)
        
    except Exception as e:
        print(f"Error updating product metrics: {e}")