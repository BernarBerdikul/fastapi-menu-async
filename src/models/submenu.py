import uuid as uuid_pkg
from typing import Optional

from sqlmodel import Field, SQLModel, Relationship
from src.models.mixins import TimestampMixin, UUIDMixin

__all__ = (
    'Submenu',
    'SubmenuRead',
    'SubmenuList',
    'SubmenuDetail',
    'SubmenuCreate',
    'SubmenuUpdate',
)


class SubmenuBase(SQLModel):
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


class Submenu(TimestampMixin, SubmenuBase, table=True):
    __tablename__ = 'submenu'

    is_removed: bool = Field(
        title="Флаг удаления",
        default=False,
        nullable=False,
    )
    parent_id: uuid_pkg.UUID = Field(
        title='Идентификатор родительского меню',
        default=None,
        nullable=True,
        foreign_key='menu.id',
    )
    parent: 'Menu' = Relationship(
        back_populates='children',
    )
    submenu_dishes: list['Dish'] = Relationship(
        back_populates='submenu',
        sa_relationship_kwargs={
            "uselist": True,
            "cascade": "all, delete",
        },
    )


class SubmenuRead(SubmenuBase, UUIDMixin):
    dishes_count: int = Field(default=0)


class SubmenuList(SQLModel):
    __root__: list[SubmenuRead]


class SubmenuDetail(SubmenuRead):
    ...


class SubmenuCreate(SubmenuBase):
    parent_id: Optional[uuid_pkg.UUID]

    class Config:
        schema_extra = {
            "example": {
                "title": "My submenu",
                "description": "My submenu's description",
            }
        }


class SubmenuUpdate(SubmenuBase):
    title: Optional[str] = Field(
        title='Наименование меню',
        max_length=30,
    )
    description: Optional[str] = Field(
        title='Описание меню',
        max_length=255,
    )

    class Config:
        schema_extra = {
            "example": {
                "title": "My updated submenu",
                "description": "My updated submenu's description",
            }
        }
