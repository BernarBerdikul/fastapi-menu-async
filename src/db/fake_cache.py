from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from src.db.cache import AbstractCache

__all__ = ('FakeCache',)


@dataclass
class FakeCache(AbstractCache):
    cache: Dict[str, Any] = field(default_factory=dict)

    async def get(self, name: str) -> Optional[dict]:
        return self.cache.get(name)

    async def set(self, name: str, value: Any, expire: Optional[int] = None):
        self.cache.update({name: value})

    async def delete(self, name: str) -> None:
        self.cache.pop(name)

    async def close(self) -> None:
        self.cache = {}
