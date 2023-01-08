from abc import ABC, abstractmethod
from typing import Optional, Union


class AbstractCache(ABC):

    @abstractmethod
    async def get(self, name: str):
        raise NotImplementedError

    @abstractmethod
    async def set(self, name: str, value: Union[bytes, str], expire: Optional[int] = None):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, name: str):
        raise NotImplementedError

    @abstractmethod
    async def close(self):
        raise NotImplementedError


cache: Optional[AbstractCache] = None


# Функция понадобится при внедрении зависимостей
async def get_cache() -> AbstractCache:
    return cache
