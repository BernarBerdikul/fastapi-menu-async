import uuid as uuid_pkg

from sqlmodel import Field, Relationship, SQLModel

from src.models.mixins import TimestampMixin, UUIDMixin

__all__ = (
    "Submenu",
    "SubmenuRead",
    "SubmenuList",
    "SubmenuDetail",
    "SubmenuCreate",
    "SubmenuUpdate",
)


class SubmenuBase(SQLModel):
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


class Submenu(TimestampMixin, SubmenuBase, table=True):  # type: ignore
    __tablename__ = "submenu"  # noqa

    is_removed: bool = Field(
        title="Флаг удаления",
        default=False,
        nullable=False,
    )
    parent_id: uuid_pkg.UUID = Field(
        title="Идентификатор родительского меню",
        default=None,
        nullable=True,
        foreign_key="menu.id",
    )
    parent: "Menu" = Relationship(  # type: ignore
        back_populates="children",
    )
    submenu_dishes: list["Dish"] = Relationship(  # type: ignore
        back_populates="submenu",
        sa_relationship_kwargs={
            "uselist": True,
            "cascade": "all, delete",
        },
    )


class SubmenuRead(SubmenuBase, UUIDMixin):
    dishes_count: int | None = Field(default=0)


class SubmenuList(SQLModel):
    __root__: list[SubmenuRead]


class SubmenuDetail(SubmenuRead):
    ...


class SubmenuCreate(SubmenuBase):
    parent_id: uuid_pkg.UUID | None

    class Config:
        schema_extra = {
            "example": {
                "title": "My submenu",
                "description": "My submenu description",
            },
        }


class SubmenuUpdate(SQLModel):
    title: str | None = Field(
        title="Наименование меню",
        max_length=30,
    )
    description: str | None = Field(
        title="Описание меню",
        max_length=255,
    )

    class Config:
        schema_extra = {
            "example": {
                "title": "My updated submenu",
                "description": "My updated submenu description",
            },
        }
