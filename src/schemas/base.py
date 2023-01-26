import orjson
from pydantic import BaseModel

__all__ = (
    "FastJsonModel",
    "CamelJsonModel",
    "CamelJsonOrmModel",
)


def to_camel(string: str) -> str:
    new_str = "".join(word.capitalize() for word in string.split("_"))
    return f"{new_str[0].lower()}{new_str[1:]}"


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class FastJsonModel(BaseModel):
    """Модель с быстрым json-сериализатором."""

    # Standard config settings.
    class Config:
        arbitrary_types_allowed = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class CamelJsonModel(FastJsonModel):
    """Модель с поддержкой сериализаций в camelCase."""

    # Camel config settings.
    class Config:
        # Camelize will give us camelCase field names for external usage (docs, client-side app, etc.)
        # while maintaining snake_case for internal usage.
        alias_generator = to_camel
        # Allow internal usage of snake_case field names.
        allow_population_by_field_name = True
        # Extra whitespace? Gross.
        anystr_strip_whitespace = True


class CamelJsonOrmModel(CamelJsonModel):
    """Модель с поддержкой ORM сериализаций данных."""

    class Config:
        orm_mode = True
