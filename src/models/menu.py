from sqlmodel import Field, Relationship, SQLModel

from src.models.mixins import TimestampMixin, UUIDMixin

__all__ = (
    "Menu",
    "MenuRead",
    "MenuList",
    "MenuCreate",
    "MenuUpdate",
)


class MenuBase(SQLModel):
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


class Menu(TimestampMixin, MenuBase, table=True):  # type: ignore
    __tablename__ = "menu"  # noqa

    is_removed: bool = Field(
        title="Флаг удаления",
        default=False,
        nullable=False,
    )
    children: list["Submenu"] = Relationship(  # type: ignore
        back_populates="parent",
        sa_relationship_kwargs={
            "uselist": True,
            "cascade": "all, delete",
        },
    )
    menu_dishes: list["Dish"] = Relationship(  # type: ignore
        back_populates="menu",
        sa_relationship_kwargs={
            "uselist": True,
            "cascade": "all, delete",
        },
    )


class MenuRead(MenuBase, UUIDMixin):
    submenus_count: int | None = Field(default=0)
    dishes_count: int | None = Field(default=0)


class MenuList(SQLModel):
    __root__: list[MenuRead]


class MenuCreate(MenuBase):
    ...

    class Config:
        schema_extra = {
            "example": {
                "title": "My menu",
                "description": "My menu description",
            },
        }


class MenuUpdate(SQLModel):
    title: str | None = Field(title="Наименование меню", max_length=30)
    description: str | None = Field(title="Описание меню", max_length=255)

    class Config:
        schema_extra = {
            "example": {
                "title": "My updated menu",
                "description": "My updated menu description",
            },
        }
