import uuid as uuid_pkg
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from src.models.mixins import TimestampMixin, UUIDMixin

__all__ = (
    'Menu',
    'MenuRead',
    'MenuList',
    'MenuDetail',
    'MenuCreate',
    'MenuUpdate',
)


class MenuBase(SQLModel):
    title: str = Field(
        title='Наименование меню',
        max_length=30,
        nullable=False,
    )
    description: str = Field(
        title='Описание меню',
        max_length=255,
        nullable=False,
    )


class Menu(TimestampMixin, MenuBase, table=True):
    __tablename__ = 'menu'

    is_removed: bool = Field(
        title="Флаг удаления",
        default=False,
        nullable=False,
    )
    children: list['Submenu'] = Relationship(
        back_populates='parent',
        sa_relationship_kwargs={
            "uselist": True,
            "cascade": 'all, delete',
        },
    )
    menu_dishes: list['Dish'] = Relationship(
        back_populates='menu',
        sa_relationship_kwargs={
            "uselist": True,
            "cascade": "all, delete",
        },
    )


class MenuRead(MenuBase, UUIDMixin):
    submenus_count: int = Field(default=0)
    dishes_count: int = Field(default=0)


class MenuList(SQLModel):
    __root__: list[MenuRead]


class MenuDetailItem(MenuBase, UUIDMixin):
    ...


class MenuDetail(MenuRead):
    submenus: list[MenuDetailItem]


class MenuCreate(MenuBase):
    ...

    class Config:
        schema_extra = {
            "example": {
                "title": "My menu",
                "description": "My menu's description",
            }
        }


class MenuUpdate(MenuBase):
    title: Optional[str] = Field(title='Наименование меню', max_length=30)
    description: Optional[str] = Field(title='Описание меню', max_length=255)

    class Config:
        schema_extra = {
            "example": {
                "title": "My updated menu",
                "description": "My updated menu's description",
            }
        }
