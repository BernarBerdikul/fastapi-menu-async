__all__ = ("StatusMessage",)

from src.schemas.base import CamelJsonModel


class StatusMessage(CamelJsonModel):
    status: bool
    message: str
