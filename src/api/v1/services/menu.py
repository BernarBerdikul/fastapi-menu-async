import uuid as uuid_pkg
from dataclasses import dataclass, field
from http import HTTPStatus

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.services import ServiceMixin
from src.db.cache import AbstractCache, get_cache
from src.db.db import get_async_session
from src.models import MenuCreate, MenuList, MenuRead, MenuUpdate

__all__ = (
    "MenuService",
    "get_menu_service",
)

from src.repositories import MenuRepository


@dataclass
class MenuService(ServiceMixin):
    cache_key: str = field(default="menu-list")

    async def get_list(self) -> MenuList:
        """Получить список меню."""
        if cached_menus := await self.cache.get(name=self.cache_key):
            return cached_menus

        menus = await self.repository.list()
        if serialized_menus := MenuList.from_orm(menus):
            await self.cache.set(name=self.cache_key, value=serialized_menus.json())
        return serialized_menus

    async def get_detail(self, menu_id: uuid_pkg.UUID) -> MenuRead:
        """Получить детальную информацию по меню."""
        if cached_menu := await self.cache.get(name=f"{menu_id}"):
            return cached_menu

        menu = await self.repository.get(menu_id=menu_id)
        if not menu:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="menu not found",
            )

        if serialized_menu := MenuRead.from_orm(menu):
            await self.cache.set(name=f"{menu_id}", value=serialized_menu.json())
        return serialized_menu

    async def create(self, data: MenuCreate) -> MenuRead:
        """Создать меню."""
        new_menu = await self.repository.add(data=data)
        await self.cache.delete(name=self.cache_key)
        return MenuRead.from_orm(new_menu)

    async def update(self, menu_id: uuid_pkg.UUID, data: MenuUpdate) -> MenuRead:
        """Обновить меню."""
        updated_menu = await self.repository.update(menu_id=menu_id, data=data)
        if not updated_menu:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="menu not found",
            )
        await self.cache.delete(name=f"{menu_id}")
        await self.cache.delete(name=self.cache_key)
        return MenuRead.from_orm(updated_menu)

    async def delete(self, menu_id: uuid_pkg.UUID) -> bool:
        """Удалить меню."""
        is_deleted = await self.repository.delete(menu_id=menu_id)
        await self.cache.delete(name=f"{menu_id}")
        await self.cache.delete(name=self.cache_key)
        return is_deleted


async def get_menu_service(
    cache: AbstractCache = Depends(get_cache),
    session: AsyncSession = Depends(get_async_session),
) -> MenuService:
    repository = MenuRepository(session=session)
    return MenuService(cache=cache, repository=repository)
