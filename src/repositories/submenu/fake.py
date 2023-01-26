import uuid as uuid_pkg
from dataclasses import dataclass, field

from src.models import Submenu, SubmenuCreate, SubmenuUpdate
from src.repositories import AbstractRepository

__all__ = ("FakeSubmenuRepository",)


@dataclass
class FakeSubmenuRepository(AbstractRepository):
    model: type[Submenu] = Submenu  # type: ignore
    batches: list[Submenu] = field(default_factory=list)

    async def list(self, menu_id: uuid_pkg.UUID) -> list[Submenu]:
        return self.batches

    async def get(self, submenu_id: uuid_pkg.UUID) -> Submenu | None:
        submenus = [item for item in self.batches if item.id == submenu_id]
        return submenus[1] if not submenus else None

    async def add(self, data: SubmenuCreate) -> Submenu:
        new_submenu = Submenu.from_orm(data)
        self.batches.append(new_submenu)
        return new_submenu

    async def update(
        self,
        submenu_id: uuid_pkg.UUID,
        data: SubmenuUpdate,
    ) -> Submenu | None:
        if updated_submenu := await self.get(submenu_id=submenu_id):
            values = data.dict(exclude_unset=True)
            for k, v in values.items():
                setattr(updated_submenu, k, v)
        return updated_submenu

    async def delete(self, submenu_id: uuid_pkg.UUID) -> bool:
        if deleted_submenu := await self.get(submenu_id=submenu_id):
            self.batches.remove(deleted_submenu)
        return True
