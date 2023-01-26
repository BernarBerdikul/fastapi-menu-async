from dataclasses import dataclass
from typing import Any

import orjson
from aioredis import Redis

from src import settings
from src.db.cache import AbstractCache

__all__ = ("RedisCache",)


@dataclass
class RedisCache(AbstractCache):
    cache: Redis

    async def get(self, name: str) -> Any | None:
        data = await self.cache.get(name=name)
        return orjson.loads(data) if data else None

    async def set(
        self,
        name: str,
        value: Any,
        expire: int = settings.redis.cache_expire_time,
    ) -> None:
        data = value
        if not isinstance(value, bytes | str):
            data = orjson.dumps(value)
        await self.cache.set(name=name, value=data, ex=expire)

    async def delete(self, name: str) -> None:
        await self.cache.delete(name)

    async def close(self) -> None:
        await self.cache.close()
