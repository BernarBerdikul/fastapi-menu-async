import uuid as uuid_pkg
from dataclasses import dataclass, field
from http import HTTPStatus

import orjson
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.repositories.dish import DishRepository
from src.api.v1.services import ServiceMixin
from src.db.cache import AbstractCache, get_cache
from src.db.db import get_async_session
from src.models import DishCreate, DishList, DishRead, DishUpdate

__all__ = (
    'DishService',
    'get_dish_service',
)


@dataclass
class DishService(ServiceMixin):
    repository: DishRepository
    cache_key: str = field(default='dish-list')

    async def get_list(self, submenu_id: uuid_pkg.UUID) -> DishList:
        """Получить список блюд."""
        if cached_dishes := await self.cache.get(name=self.cache_key):
            return orjson.loads(cached_dishes)

        dishes = await self.repository.list(submenu_id=submenu_id)
        if serialized_dishes := DishList.from_orm(dishes):
            await self.cache.set(name=self.cache_key, value=serialized_dishes.json())
        return serialized_dishes

    async def get_detail(self, dish_id: uuid_pkg.UUID) -> DishRead:
        """Получить детальную информацию по блюду."""
        if cached_dish := await self.cache.get(name=f'{dish_id}'):
            return orjson.loads(cached_dish)

        dish = await self.repository.get(dish_id=dish_id)
        if not dish:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='dish not found',
            )

        if serialized_dish := DishRead.from_orm(dish):
            await self.cache.set(name=f'{dish_id}', value=serialized_dish.json())
        return serialized_dish

    async def create(self, menu_id: uuid_pkg.UUID, submenu_id: uuid_pkg.UUID, data: DishCreate) -> DishRead:
        """Создать блюдо."""
        data.menu_id = menu_id
        data.submenu_id = submenu_id
        new_dish = await self.repository.add(data=data)
        await self.cache.delete(name=f'{menu_id}')
        await self.cache.delete(name=f'{submenu_id}')
        await self.cache.delete(name='menu-list')
        await self.cache.delete(name='submenu-list')
        await self.cache.delete(name=self.cache_key)
        return DishRead.from_orm(new_dish)

    async def update(self, dish_id: uuid_pkg.UUID, data: DishUpdate) -> DishRead:
        """Обновить блюдо."""
        updated_dish = await self.repository.update(dish_id=dish_id, data=data)
        if not updated_dish:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='dish not found',
            )
        await self.cache.delete(name=f'{dish_id}')
        await self.cache.delete(name=self.cache_key)
        return DishRead.from_orm(updated_dish)

    async def delete(self, dish_id: uuid_pkg.UUID) -> bool:
        """Удалить блюдо."""
        is_deleted = await self.repository.delete(dish_id=dish_id)
        await self.cache.delete(name=f'{dish_id}')
        await self.cache.delete(name=self.cache_key)
        return is_deleted


async def get_dish_service(
    cache: AbstractCache = Depends(get_cache),
    session: AsyncSession = Depends(get_async_session),
) -> DishService:
    repository = DishRepository(session=session)
    return DishService(cache=cache, session=session, repository=repository)
