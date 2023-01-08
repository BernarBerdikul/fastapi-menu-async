from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.cache import AbstractCache


@dataclass
class ServiceMixin:
    cache: AbstractCache
    session: AsyncSession
