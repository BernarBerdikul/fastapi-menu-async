import uuid as uuid_pkg

from pydantic import condecimal
from sqlmodel import Field, Relationship, SQLModel

from src.models.mixins import TimestampMixin, UUIDMixin

__all__ = (
    "Dish",
    "DishList",
    "DishRead",
    "DishCreate",
    "DishUpdate",
)


class DishBase(SQLModel):

    title: str = Field(
        title="Наименование меню",
        max_length=30,
        nullable=False,
    )
    description: str = Field(
        title="Описание меню",
        max_length=255,
        nullable=False,
    )
    price: condecimal(max_digits=8, decimal_places=2) = Field(  # type: ignore
        title="Цена блюда",
        nullable=False,
    )


class Dish(TimestampMixin, DishBase, table=True):  # type: ignore
    __tablename__ = "dish"  # noqa

    is_removed: bool = Field(
        title="Флаг удаления",
        default=False,
        nullable=False,
    )

    menu_id: uuid_pkg.UUID = Field(
        title="Идентификатор меню",
        foreign_key="menu.id",
        nullable=False,
        index=True,
    )
    menu: "Menu" = Relationship(  # type: ignore
        back_populates="menu_dishes",
    )

    submenu_id: uuid_pkg.UUID = Field(
        title="Идентификатор подменю",
        foreign_key="submenu.id",
        nullable=False,
        index=True,
    )
    submenu: "Submenu" = Relationship(  # type: ignore
        back_populates="submenu_dishes",
    )


class DishRead(DishBase, UUIDMixin):
    price: str


class DishList(SQLModel):
    __root__: list[DishRead]


class DishCreate(DishBase):
    menu_id: uuid_pkg.UUID | None
    submenu_id: uuid_pkg.UUID | None

    class Config:
        schema_extra = {
            "example": {
                "title": "My dish",
                "description": "My dish description",
                "price": 1000.00,
            },
        }


class DishUpdate(SQLModel):
    title: str | None = Field(title="Наименование меню", max_length=30)
    description: str | None = Field(title="Описание меню", max_length=255)
    price: condecimal(max_digits=8, decimal_places=2) | None = Field(  # type: ignore
        title="Цена блюда",
    )

    class Config:
        schema_extra = {
            "example": {
                "title": "My updated dish",
                "description": "My updated dish description",
                "price": 1200.00,
            },
        }
