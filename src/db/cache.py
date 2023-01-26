from abc import ABC, abstractmethod
from typing import Any


class AbstractCache(ABC):
    @abstractmethod
    async def get(self, name: str) -> Any | None:
        raise NotImplementedError

    @abstractmethod
    async def set(self, name: str, value: Any, expire: int = 0) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError


cache: AbstractCache | None = None


# Функция понадобится при внедрении зависимостей
async def get_cache() -> AbstractCache | None:
    return cache
