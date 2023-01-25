from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v2.repositories import DishRepository, MenuRepository, SubmenuRepository
from src.uow import AbstractUnitOfWork


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session: AsyncSession):
        self.session = session
        self.menu_repo: MenuRepository = MenuRepository(session=self.session)
        self.submenu_repo: SubmenuRepository = SubmenuRepository(
            session=self.session,
        )
        self.dish_repo: DishRepository = DishRepository(session=self.session)

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
