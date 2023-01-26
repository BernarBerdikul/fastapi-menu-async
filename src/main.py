import aioredis  # noqa
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src import settings
from src.api.v1.resources import dishes as dishes_v1
from src.api.v1.resources import menus as menus_v1
from src.api.v1.resources import submenus as submenus_v1
from src.api.v2.resources import dishes as dishes_v2
from src.api.v2.resources import menus as menus_v2
from src.api.v2.resources import submenus as submenus_v2
from src.db import cache, dummy_cache, redis_cache  # noqa
from src.middlewares import add_process_time_header
from src.schemas import HealthCheck

app = FastAPI(
    title=settings.app.project_name,
    description=settings.app.description,
    version=settings.app.version,
    # Адрес документации в красивом интерфейсе
    docs_url="/api/openapi",
    redoc_url="/api/redoc",
    # Адрес документации в формате OpenAPI
    openapi_url=f"{settings.app.api_doc_prefix}/openapi.json",
    debug=settings.app.debug,
    default_response_class=ORJSONResponse,
)

app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)


# Подключаем роутеры к серверу
# API version 1
app.include_router(router=menus_v1.router, prefix="/api/v1")
app.include_router(router=submenus_v1.router, prefix="/api/v1")
app.include_router(router=dishes_v1.router, prefix="/api/v1")
# API version 2
app.include_router(router=menus_v2.router, prefix="/api/v2")
app.include_router(router=submenus_v2.router, prefix="/api/v2")
app.include_router(router=dishes_v2.router, prefix="/api/v2")


@app.get("/", response_model=HealthCheck, tags=["status"])
async def health_check():
    return {
        "service": settings.app.project_name,
        "version": settings.app.version,
        "description": settings.app.description,
    }


@app.on_event("startup")
async def startup():
    """Подключаемся к базам при старте сервера"""
    # Redis cache
    cache.cache = redis_cache.RedisCache(
        cache=await aioredis.Redis(
            host=settings.redis.host,
            port=settings.redis.port,
            db=settings.redis.db,
            encoding=settings.redis.encoding,
            max_connections=settings.redis.max_connections,
        ),
    )
    # Dummy cache
    # cache.cache = dummy_cache.DummyCache()


@app.on_event("shutdown")
async def shutdown():
    """Отключаемся от баз при выключении сервера"""
    await cache.cache.close()


if __name__ == "__main__":
    # Приложение может запускаться командой
    # `uvicorn main:app --host 0.0.0.0 --port 8000`
    # но чтобы не терять возможность использовать дебагер,
    # запустим uvicorn сервер через python
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
