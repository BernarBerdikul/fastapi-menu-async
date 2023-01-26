import uuid as uuid_pkg
from dataclasses import dataclass, field
from http import HTTPStatus

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.services import ServiceMixin
from src.db.cache import AbstractCache, get_cache
from src.db.db import get_async_session
from src.models import (
    SubmenuCreate,
    SubmenuDetail,
    SubmenuList,
    SubmenuRead,
    SubmenuUpdate,
)

__all__ = (
    "SubmenuService",
    "get_submenu_service",
)

from src.repositories import SubmenuRepository


@dataclass
class SubmenuService(ServiceMixin):
    cache_key: str = field(default="submenu-list")

    async def get_list(self, menu_id: uuid_pkg.UUID) -> SubmenuList:
        """Получить список подменю."""
        if cached_submenus := await self.cache.get(name=self.cache_key):
            return cached_submenus

        submenus = await self.repository.list(menu_id=menu_id)
        if serialized_submenus := SubmenuList.from_orm(submenus):
            await self.cache.set(name=self.cache_key, value=serialized_submenus.json())
        return serialized_submenus

    async def get_detail(self, submenu_id: uuid_pkg.UUID) -> SubmenuDetail:
        """Получить детальную информацию по подменю."""
        if cached_submenu := await self.cache.get(name=f"{submenu_id}"):
            return cached_submenu

        submenu = await self.repository.get(submenu_id=submenu_id)
        if not submenu:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="submenu not found",
            )

        if serialized_submenu := SubmenuDetail.from_orm(submenu):
            await self.cache.set(name=f"{submenu_id}", value=serialized_submenu.json())
        return serialized_submenu

    async def create(self, menu_id: uuid_pkg.UUID, data: SubmenuCreate) -> SubmenuRead:
        """Создать подменю."""
        data.parent_id = menu_id
        new_submenu = await self.repository.add(data=data)
        await self.cache.delete(name=f"{menu_id}")
        await self.cache.delete(name="menu-list")
        await self.cache.delete(name=self.cache_key)
        return SubmenuRead.from_orm(new_submenu)

    async def update(
        self,
        submenu_id: uuid_pkg.UUID,
        data: SubmenuUpdate,
    ) -> SubmenuRead:
        """Обновить подменю."""
        updated_submenu = await self.repository.update(submenu_id=submenu_id, data=data)
        if not updated_submenu:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="submenu not found",
            )
        await self.cache.delete(name=f"{submenu_id}")
        await self.cache.delete(name=self.cache_key)
        return SubmenuRead.from_orm(updated_submenu)

    async def delete(self, menu_id: uuid_pkg.UUID, submenu_id: uuid_pkg.UUID) -> bool:
        """Удалить подменю."""
        is_deleted = await self.repository.delete(submenu_id=submenu_id)
        await self.cache.delete(name=f"{submenu_id}")
        await self.cache.delete(name=f"{menu_id}")
        await self.cache.delete(name=self.cache_key)
        return is_deleted


async def get_submenu_service(
    cache: AbstractCache = Depends(get_cache),
    session: AsyncSession = Depends(get_async_session),
) -> SubmenuService:
    repository = SubmenuRepository(session=session)
    return SubmenuService(cache=cache, repository=repository)
