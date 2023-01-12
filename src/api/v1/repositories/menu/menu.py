import uuid as uuid_pkg
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from src.api.v1.repositories.menu.base import AbstractMenuRepository
from src.models import Menu, MenuCreate, MenuUpdate, Submenu

__all__ = ('MenuRepository',)


class MenuRepository(AbstractMenuRepository):
    model: Menu = Menu

    async def list(self) -> list[Menu]:
        statement = select(
            self.model.id,
            self.model.title,
            self.model.description,
            func.count(self.model.children).label('submenus_count'),
            func.count(self.model.menu_dishes).label('dishes_count'),
        ).outerjoin(
            self.model.children,
        ).outerjoin(
            self.model.menu_dishes,
        ).group_by(
            self.model.id,
            self.model.title,
            self.model.description,
        )
        results = await self.session.execute(statement)
        menus: list[Menu] = results.all()
        return menus

    async def get(self, menu_id: uuid_pkg.UUID) -> Optional[Menu]:
        submenus = func.json_agg(
            func.json_build_object(
                'id',
                Submenu.id,
                'title',
                Submenu.title,
                'description',
                Submenu.description,
            ),
        )
        statement = select(
            self.model.id,
            self.model.title,
            self.model.description,
            submenus.label('submenus'),
            func.count(self.model.children).label('submenus_count'),
            func.count(self.model.menu_dishes).label('dishes_count'),
        ).outerjoin(
            self.model.children,
        ).outerjoin(
            self.model.menu_dishes,
        ).where(
            self.model.id == menu_id,
        ).group_by(
            self.model.id,
            self.model.title,
            self.model.description,
        )
        results = await self.session.execute(statement=statement)
        menu: Optional[Menu] = results.one_or_none()
        return menu

    async def __get(self, menu_id: uuid_pkg.UUID) -> Optional[Menu]:
        statement = select(self.model).where(self.model.id == menu_id)
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
        statement = select(
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
