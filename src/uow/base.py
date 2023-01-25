from abc import ABC, abstractmethod

from src.repositories import AbstractRepository


class AbstractUnitOfWork(ABC):
    menu_repo: AbstractRepository
    submenu_repo: AbstractRepository
    dish_repo: AbstractRepository

    async def __aenter__(self, *args):
        return self

    async def __aexit__(self, *args):
        try:
            await self.commit()
        except Exception:
            await self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError
