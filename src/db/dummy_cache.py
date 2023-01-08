from dataclasses import dataclass, field
from typing import Optional, Union, Any, Dict

from src.db.cache import AbstractCache

__all__ = ('DummyCache',)


@dataclass
class DummyCache(AbstractCache):

    async def get(self, name: str) -> Optional[dict]:
        return None

    async def set(self, name: str, value: Union[bytes, str], expire: Optional[int] = None):
        return None

    async def delete(self, name: str) -> None:
        return None

    async def close(self) -> None:
        ...
