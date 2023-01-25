# import uuid as uuid_pkg
# from dataclasses import dataclass, field
# from typing import ClassVar
#
# from src.models import Submenu, SubmenuCreate, SubmenuUpdate
# from src.repositories import AbstractRepository
#
# __all__ = ('FakeSubmenuRepository',)
#
#
# @dataclass
# class FakeSubmenuRepository(AbstractRepository):
#     model: ClassVar[Submenu] = Submenu
#     batches: list[Submenu] = field(default_factory=list)
#
#     async def list(self, menu_id: uuid_pkg.UUID) -> list[Submenu]:
#         return self.batches
#
#     async def get(self, submenu_id: uuid_pkg.UUID) -> Submenu | None:
#         return self.batches[1]
#
#     async def __get(self, submenu_id: uuid_pkg.UUID) -> Submenu | None:
#         return self.batches[1]
#
#     async def add(self, data: SubmenuCreate) -> Submenu:
#         new_submenu = Submenu.from_orm(data)
#         self.batches.append(new_submenu)
#         return new_submenu
#
#     async def update(self, submenu_id: uuid_pkg.UUID, data: SubmenuUpdate) -> Submenu | None:
#         self.batches[1] = data
#         return data
#
#     async def delete(self, submenu_id: uuid_pkg.UUID) -> bool:
#         self.batches.append(new_submenu)
#         return True
