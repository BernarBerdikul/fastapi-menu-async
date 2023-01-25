from dataclasses import dataclass

from src.db import dummy_cache
from src.db.cache import AbstractCache
from src.uow import AbstractUnitOfWork


@dataclass
class ServiceMixin:
    cache: AbstractCache
    uow: AbstractUnitOfWork

    def __post_init__(self):
        if self.cache is None:
            self.cache = dummy_cache.DummyCache()
