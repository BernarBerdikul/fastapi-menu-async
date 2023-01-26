import uuid as uuid_pkg

import sqlalchemy as sa
from sqlalchemy.orm import joinedload

from src.models import Dish, Menu, MenuCreate, MenuUpdate, Submenu
from src.repositories import AbstractRepository

__all__ = ("MenuRepository",)


class MenuRepository(AbstractRepository):
    model: type[Menu] = Menu

    async def list(self) -> list[Menu]:
        statement = (
            sa.select(
                self.model.id,
                self.model.title,
                self.model.description,
                sa.func.coalesce(
                    sa.func.count(
                        sa.func.distinct(
                            Submenu.id,
                        ),
                    ),
                    0,
                ).label("submenus_count"),
                sa.func.coalesce(
                    sa.func.count(Dish.id),
                    0,
                ).label("dishes_count"),
            )
            .outerjoin(
                Submenu,
                self.model.id == Submenu.parent_id,
            )
            .outerjoin(
                Dish,
                Submenu.id == Dish.submenu_id,
            )
            .group_by(Menu.id)
        )
        results = await self.session.execute(statement)
        menus: list[Menu] = results.all()
        return menus

    async def get(self, menu_id: uuid_pkg.UUID) -> Menu | None:
        statement = (
            sa.select(
                self.model.id,
                self.model.title,
                self.model.description,
                sa.func.coalesce(
                    sa.func.count(
                        sa.func.distinct(
                            Submenu.id,
                        ),
                    ),
                    0,
                ).label("submenus_count"),
                sa.func.coalesce(
                    sa.func.count(Dish.id),
                    0,
                ).label("dishes_count"),
            )
            .outerjoin(
                Submenu,
                self.model.id == Submenu.parent_id,
            )
            .outerjoin(
                Dish,
                Submenu.id == Dish.submenu_id,
            )
            .where(
                self.model.id == menu_id,
            )
            .group_by(Menu.id)
        )
        results = await self.session.execute(statement=statement)
        menu: Menu | None = results.one_or_none()
        return menu

    async def __get(self, menu_id: uuid_pkg.UUID) -> Menu | None:
        statement = sa.select(self.model).where(self.model.id == menu_id)
        results = await self.session.execute(statement=statement)
        menu: Menu | None = results.scalar_one_or_none()
        return menu

    async def add(self, data: MenuCreate) -> Menu:
        new_menu = Menu.from_orm(data)
        self.session.add(new_menu)
        await self.session.commit()
        await self.session.refresh(new_menu)
        return new_menu

    async def update(self, menu_id: uuid_pkg.UUID, data: MenuUpdate) -> Menu | None:
        if updated_menu := await self.__get(menu_id=menu_id):
            values = data.dict(exclude_unset=True)
            for k, v in values.items():
                setattr(updated_menu, k, v)
            self.session.add(updated_menu)
            await self.session.commit()
            await self.session.refresh(updated_menu)
        return updated_menu

    async def delete(self, menu_id: uuid_pkg.UUID) -> bool:
        statement = (
            sa.select(
                self.model,
            )
            .options(
                joinedload(self.model.children),
                joinedload(self.model.menu_dishes),
            )
            .where(
                self.model.id == menu_id,
            )
        )
        menu = await self.session.scalar(statement)
        if menu:
            await self.session.delete(menu)
            await self.session.commit()
        return True
