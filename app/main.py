from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import generate_latest, REGISTRY
import time
import asyncio

from app.api.users import router as users_router
from app.api.products import router as products_router
from app.api.metrics_endpoints import router as metrics_router
from app.core.metrics import (
    http_requests_total, 
    http_request_duration_seconds,
    http_errors_total,
    app_info
)
from app.db.session import AsyncSessionLocal

app = FastAPI(title="Lab 7 - Monitoring")

# Встановлюємо інформацію про додаток
app_info.info({"version": "0.1.0", "service": "FastAPI Lab 7"})

# Підключаємо роутери
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(products_router, prefix="/store", tags=["store"])
app.include_router(metrics_router, prefix="/api", tags=["Metrics"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Lab 7 - Monitoring with Prometheus & Grafana"}

# ============= PROMETHEUS METRICS =============

@app.get("/metrics")
async def metrics():
    """Endpoint для Prometheus щоб збирати метрики"""
    return Response(generate_latest(REGISTRY), media_type="text/plain")

# ============= MIDDLEWARE для відслідження метрик =============

@app.middleware("http")
async def track_http_metrics(request, call_next):
    """Middleware для відслідження HTTP метрик"""
    start_time = time.time()
    
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        
        # Записуємо метрики
        http_requests_total.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        http_request_duration_seconds.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)
        
        # Записуємо помилки (4xx, 5xx)
        if response.status_code >= 400:
            http_errors_total.labels(
                method=request.method,
                endpoint=request.url.path,
                status_code=response.status_code
            ).inc()
        
        return response
        
    except Exception as e:
        duration = time.time() - start_time
        
        http_requests_total.labels(
            method=request.method,
            endpoint=request.url.path,
            status=500
        ).inc()
        
        http_errors_total.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=500
        ).inc()
        
        raise