__all__ = ("HealthCheck",)

from src.schemas.base import CamelJsonModel


class HealthCheck(CamelJsonModel):
    service: str
    version: str
    description: str
