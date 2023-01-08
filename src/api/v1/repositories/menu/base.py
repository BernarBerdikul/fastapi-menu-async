import uuid as uuid_pkg
from abc import ABC, abstractmethod
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import MenuCreate, MenuUpdate

__all__ = ("AbstractMenuRepository",)


@dataclass
class AbstractMenuRepository(ABC):
    session: AsyncSession

    @abstractmethod
    async def get(self, menu_id: uuid_pkg.UUID):
        raise NotImplementedError

    @abstractmethod
    async def list(self):
        raise NotImplementedError

    @abstractmethod
    async def add(self, data: MenuCreate):
        raise NotImplementedError

    @abstractmethod
    async def update(self, menu_id: uuid_pkg.UUID, data: MenuUpdate):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, menu_id: uuid_pkg.UUID):
        raise NotImplementedError
