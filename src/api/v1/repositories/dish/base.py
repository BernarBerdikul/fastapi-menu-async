import uuid as uuid_pkg
from abc import ABC, abstractmethod
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import DishCreate, DishUpdate

__all__ = ('AbstractDishRepository',)


@dataclass
class AbstractDishRepository(ABC):
    session: AsyncSession

    @abstractmethod
    async def get(self, dish_id: uuid_pkg.UUID):
        raise NotImplementedError

    @abstractmethod
    async def list(self, submenu_id: uuid_pkg.UUID):
        raise NotImplementedError

    @abstractmethod
    async def add(self, data: DishCreate):
        raise NotImplementedError

    @abstractmethod
    async def update(self, dish_id: uuid_pkg.UUID, data: DishUpdate):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, dish_id: uuid_pkg.UUID):
        raise NotImplementedError
