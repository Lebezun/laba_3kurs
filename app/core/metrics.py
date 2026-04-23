from prometheus_client import Counter, Histogram, Gauge

# --- Стандартні HTTP метрики ---
http_requests_total = Counter(
    "http_requests_total", 
    "Total number of HTTP requests", 
    ["method", "endpoint", "status"]
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds", 
    "HTTP request duration in seconds", 
    ["method", "endpoint"]
)

http_errors_total = Counter(
    "http_errors_total", 
    "Total number of HTTP errors", 
    ["method", "endpoint", "status_code"]
)

# --- Метрики продуктів (те, що вимагає твій CRUD) ---
products_created_total = Counter(
    "products_created_total", 
    "Total number of created products"
)

products_deleted_total = Counter(
    "products_deleted_total", 
    "Total number of deleted products"
)

products_updated_total = Counter(
    "products_updated_total", 
    "Total number of updated products"
)

# --- Твоя головна метрика для Лаби 7 ---
total_purchases_price = Gauge(
    "total_purchases_price", 
    "Сумарна ціна всіх покупок"
)