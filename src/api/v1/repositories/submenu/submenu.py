import uuid as uuid_pkg
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from src.api.v1.repositories.submenu import AbstractSubmenuRepository
from src.models import Submenu, SubmenuCreate, SubmenuUpdate

__all__ = ('SubmenuRepository',)


class SubmenuRepository(AbstractSubmenuRepository):
    model: Submenu = Submenu

    async def list(self, menu_id: uuid_pkg.UUID) -> list[Submenu]:
        statement = select(
            self.model.id,
            self.model.title,
            self.model.description,
            func.count(self.model.submenu_dishes).label('dishes_count'),
        ).outerjoin(
            self.model.submenu_dishes,
        ).where(
            self.model.parent_id == menu_id,
        ).group_by(
            self.model.id,
            self.model.title,
            self.model.description,
        )
        results = await self.session.execute(statement)
        submenus: list[Submenu] = results.all()
        return submenus

    async def get(self, submenu_id: uuid_pkg.UUID) -> Optional[Submenu]:
        statement = select(
            self.model.id,
            self.model.title,
            self.model.description,
            func.count(self.model.submenu_dishes).label('dishes_count'),
        ).outerjoin(
            self.model.submenu_dishes,
        ).where(
            self.model.id == submenu_id,
        ).group_by(
            self.model.id,
            self.model.title,
            self.model.description,
        )
        results = await self.session.execute(statement=statement)
        submenu: Optional[Submenu] = results.one_or_none()
        return submenu

    async def __get(self, submenu_id: uuid_pkg.UUID) -> Optional[Submenu]:
        statement = select(self.model).where(self.model.id == submenu_id)
        results = await self.session.execute(statement=statement)
        menu: Optional[Submenu] = results.scalar_one_or_none()
        return menu

    async def add(self, data: SubmenuCreate) -> Submenu:
        new_submenu = Submenu.from_orm(data)
        self.session.add(new_submenu)
        await self.session.commit()
        await self.session.refresh(new_submenu)
        return new_submenu

    async def update(self, submenu_id: uuid_pkg.UUID, data: SubmenuUpdate) -> Optional[Submenu]:
        if updated_submenu := await self.__get(submenu_id=submenu_id):
            values = data.dict(exclude_unset=True)
            for k, v in values.items():
                setattr(updated_submenu, k, v)
            self.session.add(updated_submenu)
            await self.session.commit()
            await self.session.refresh(updated_submenu)
        return updated_submenu

    async def delete(self, submenu_id: uuid_pkg.UUID) -> bool:
        statement = select(
            self.model,
        ).options(
            joinedload(self.model.submenu_dishes),
        ).where(
            self.model.id == submenu_id,
        )
        submenu = await self.session.scalar(statement)
        if submenu:
            await self.session.delete(submenu)
            await self.session.commit()
        return True
