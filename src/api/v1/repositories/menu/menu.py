import uuid as uuid_pkg
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import joinedload

from src.api.v1.repositories.menu.base import AbstractMenuRepository
from src.models import Dish, Menu, MenuCreate, MenuUpdate, Submenu

__all__ = ('MenuRepository',)


class MenuRepository(AbstractMenuRepository):
    model: Menu = Menu

    async def list(self) -> list[Menu]:
        submenus_counts = sa.select(
            Submenu.parent_id.label('menu_id'),
            sa.func.count(Submenu.id).label('count'),
        ).group_by(Submenu.parent_id).subquery()

        dishes_counts = sa.select(
            Dish.menu_id.label('menu_id'),
            sa.func.count(Dish.id).label('count'),
        ).group_by(Dish.menu_id).subquery()

        statement = sa.select(
            self.model.id,
            self.model.title,
            self.model.description,
            sa.func.coalesce(
                submenus_counts.c.count,
                0,
            ).label('submenus_count'),
            sa.func.coalesce(dishes_counts.c.count, 0).label('dishes_count'),
        ).outerjoin(
            submenus_counts,
            submenus_counts.c.menu_id == self.model.id,
        ).outerjoin(
            dishes_counts,
            dishes_counts.c.menu_id == self.model.id,
        )
        results = await self.session.execute(statement)
        menus: list[Menu] = results.all()
        return menus

    async def get(self, menu_id: uuid_pkg.UUID) -> Optional[Menu]:
        submenus_counts = sa.select(
            Submenu.parent_id.label('menu_id'),
            sa.func.count(Submenu.id).label('count'),
        ).group_by(Submenu.parent_id).subquery()

        dishes_counts = sa.select(
            Dish.menu_id.label('menu_id'),
            sa.func.count(Dish.id).label('count'),
        ).group_by(Dish.menu_id).subquery()

        statement = sa.select(
            self.model.id,
            self.model.title,
            self.model.description,
            sa.func.coalesce(
                submenus_counts.c.count,
                0,
            ).label('submenus_count'),
            sa.func.coalesce(dishes_counts.c.count, 0).label('dishes_count'),
        ).outerjoin(
            submenus_counts,
            submenus_counts.c.menu_id == self.model.id,
        ).outerjoin(
            dishes_counts,
            dishes_counts.c.menu_id == self.model.id,
        ).where(
            self.model.id == menu_id,
        )
        results = await self.session.execute(statement=statement)
        menu: Optional[Menu] = results.one_or_none()
        return menu

    async def __get(self, menu_id: uuid_pkg.UUID) -> Optional[Menu]:
        statement = sa.select(self.model).where(self.model.id == menu_id)
        results = await self.session.execute(statement=statement)
        menu: Optional[Menu] = results.scalar_one_or_none()
        return menu

    async def add(self, data: MenuCreate) -> Menu:
        new_menu = Menu.from_orm(data)
        self.session.add(new_menu)
        await self.session.commit()
        await self.session.refresh(new_menu)
        return new_menu

    async def update(self, menu_id: uuid_pkg.UUID, data: MenuUpdate) -> Optional[Menu]:
        if updated_menu := await self.__get(menu_id=menu_id):
            values = data.dict(exclude_unset=True)
            for k, v in values.items():
                setattr(updated_menu, k, v)
            self.session.add(updated_menu)
            await self.session.commit()
            await self.session.refresh(updated_menu)
        return updated_menu

    async def delete(self, menu_id: uuid_pkg.UUID) -> bool:
        statement = sa.select(
            self.model,
        ).options(
            joinedload(self.model.children),
            joinedload(self.model.menu_dishes),
        ).where(
            self.model.id == menu_id,
        )
        menu = await self.session.scalar(statement)
        if menu:
            await self.session.delete(menu)
            await self.session.commit()
        return True
