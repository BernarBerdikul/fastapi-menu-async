from dataclasses import dataclass
from typing import Any

from src.db.cache import AbstractCache

__all__ = ("DummyCache",)


@dataclass
class DummyCache(AbstractCache):
    async def get(self, name: str) -> dict | None:
        return None

    async def set(self, name: str, value: Any, expire: int = 0):
        return None

    async def delete(self, name: str) -> None:
        return None

    async def close(self) -> None:
        return None
