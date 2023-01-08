__all__ = ('StatusMessage',)

from src.api.v1.schemas.base import CamelJsonModel


class StatusMessage(CamelJsonModel):
    status: bool
    message: str
