import uuid as uuid_pkg
from dataclasses import dataclass, field
from http import HTTPStatus

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v2.services import ServiceMixin
from src.db.cache import AbstractCache, get_cache
from src.db.db import get_async_session
from src.models import MenuCreate, MenuList, MenuRead, MenuUpdate

__all__ = (
    "MenuService",
    "get_menu_service",
)

from src.uow import SqlAlchemyUnitOfWork


@dataclass
class MenuService(ServiceMixin):
    cache_key: str = field(default="menu-list")

    async def get_list(self) -> MenuList:
        """Получить список меню."""
        async with self.uow:
            if cached_menus := await self.cache.get(name=self.cache_key):
                return cached_menus

            menus = await self.uow.menu_repo.list()
            if serialized_menus := MenuList.from_orm(menus):
                await self.cache.set(name=self.cache_key, value=serialized_menus.json())
        return serialized_menus

    async def get_detail(self, menu_id: uuid_pkg.UUID) -> MenuRead:
        """Получить детальную информацию по меню."""
        async with self.uow:
            if cached_menu := await self.cache.get(name=f"{menu_id}"):
                return cached_menu

            menu = await self.uow.menu_repo.get(menu_id=menu_id)
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
        async with self.uow:
            new_menu = await self.uow.menu_repo.add(data=data)
            await self.cache.delete(name=self.cache_key)
        return MenuRead.from_orm(new_menu)

    async def update(self, menu_id: uuid_pkg.UUID, data: MenuUpdate) -> MenuRead:
        """Обновить меню."""
        async with self.uow:
            updated_menu = await self.uow.menu_repo.update(menu_id=menu_id, data=data)
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
        async with self.uow:
            is_deleted = await self.uow.menu_repo.delete(menu_id=menu_id)
            await self.cache.delete(name=f"{menu_id}")
            await self.cache.delete(name=self.cache_key)
        return is_deleted


async def get_menu_service(
    cache: AbstractCache = Depends(get_cache),
    session: AsyncSession = Depends(get_async_session),
) -> MenuService:
    uow = SqlAlchemyUnitOfWork(session=session)
    return MenuService(cache=cache, uow=uow)
