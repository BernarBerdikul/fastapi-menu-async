from dataclasses import dataclass
from typing import Optional, Union

from aioredis import Redis

from src import settings
from src.db.cache import AbstractCache

__all__ = ('RedisCache',)


@dataclass
class RedisCache(AbstractCache):
    cache: Redis

    async def get(self, name: str) -> Optional[dict]:
        return await self.cache.get(name=name)

    async def set(self, name: str, value: Union[bytes, str], expire: int = settings.redis.cache_expire_time):
        await self.cache.set(name=name, value=value, ex=expire)

    async def delete(self, name: str) -> None:
        await self.cache.delete(name)

    async def close(self) -> None:
        await self.cache.close()
