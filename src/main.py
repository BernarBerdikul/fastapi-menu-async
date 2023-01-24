import aioredis  # noqa
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src import settings
from src.api.v1.resources import dishes, menus, submenus
from src.api.v1.schemas import HealthCheck
from src.db import cache, dummy_cache, redis_cache  # noqa

app = FastAPI(
    title=settings.app.project_name,
    description=settings.app.description,
    version=settings.app.version,
    # Адрес документации в красивом интерфейсе
    docs_url='/api/openapi',
    redoc_url='/api/redoc',
    # Адрес документации в формате OpenAPI
    openapi_url=f'{settings.app.api_doc_prefix}/openapi.json',
    debug=settings.app.debug,
    default_response_class=ORJSONResponse,
)


@app.get('/', response_model=HealthCheck, tags=['status'])
async def health_check():
    return {
        'service': settings.app.project_name,
        'version': settings.app.version,
        'description': settings.app.description,
    }


@app.on_event('startup')
async def startup():
    """Подключаемся к базам при старте сервера"""
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


@app.on_event('shutdown')
async def shutdown():
    """Отключаемся от баз при выключении сервера"""
    await cache.cache.close()


# Подключаем роутеры к серверу
# app.include_router(router=main_v1_router, prefix='/api/v1')
app.include_router(router=menus.router, prefix='/api/v1')
app.include_router(router=submenus.router, prefix='/api/v1')
app.include_router(router=dishes.router, prefix='/api/v1')


if __name__ == '__main__':
    # Приложение может запускаться командой
    # `uvicorn main:app --host 0.0.0.0 --port 8000`
    # но чтобы не терять возможность использовать дебагер,
    # запустим uvicorn сервер через python
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
