from abc import ABC, abstractmethod
from typing import Any, Optional


class AbstractCache(ABC):

    @abstractmethod
    async def get(self, name: str) -> Optional[Any]:
        raise NotImplementedError

    @abstractmethod
    async def set(self, name: str, value: Any, expire: Optional[int] = None) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError


cache: Optional[AbstractCache] = None


# Функция понадобится при внедрении зависимостей
async def get_cache() -> AbstractCache:
    return cache
