import uuid as uuid_pkg
from abc import ABC, abstractmethod
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import SubmenuUpdate, SubmenuCreate

__all__ = ("AbstractSubmenuRepository",)


@dataclass
class AbstractSubmenuRepository(ABC):
    session: AsyncSession

    @abstractmethod
    async def get(self, submenu_id: uuid_pkg.UUID):
        raise NotImplementedError

    @abstractmethod
    async def list(self, menu_id: uuid_pkg.UUID):
        raise NotImplementedError

    @abstractmethod
    async def add(self, data: SubmenuCreate):
        raise NotImplementedError

    @abstractmethod
    async def update(self, submenu_id: uuid_pkg.UUID, data: SubmenuUpdate):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, submenu_id: uuid_pkg.UUID) -> bool:
        raise NotImplementedError
