import uuid as uuid_pkg
from typing import Optional

from sqlalchemy import select

from src.api.v1.repositories.dish import AbstractDishRepository
from src.models import Dish, DishCreate, DishUpdate

__all__ = ('DishRepository',)


class DishRepository(AbstractDishRepository):
    model: Dish = Dish

    async def list(self, submenu_id: uuid_pkg.UUID) -> list[Dish]:
        statement = select(
            self.model,
        ).where(
            self.model.submenu_id == submenu_id,
        )
        results = await self.session.execute(statement)
        dishes: list[Dish] = results.scalars().all()
        return dishes

    async def get(self, dish_id: uuid_pkg.UUID) -> Optional[Dish]:
        dish: Optional[Dish] = await self.session.get(self.model, dish_id)
        return dish

    async def add(self, data: DishCreate) -> Dish:
        new_dish = Dish.from_orm(data)
        self.session.add(new_dish)
        await self.session.commit()
        await self.session.refresh(new_dish)
        return new_dish

    async def update(self, dish_id: uuid_pkg.UUID, data: DishUpdate) -> Optional[Dish]:
        if updated_dish := await self.get(dish_id=dish_id):
            values = data.dict(exclude_unset=True)
            for k, v in values.items():
                setattr(updated_dish, k, v)
            self.session.add(updated_dish)
            await self.session.commit()
            await self.session.refresh(updated_dish)
        return updated_dish

    async def delete(self, dish_id: uuid_pkg.UUID) -> bool:
        dish = await self.get(dish_id=dish_id)
        if dish:
            await self.session.delete(dish)
            await self.session.commit()
        return True
