__all__ = ('HealthCheck',)

from src.api.v1.schemas.base import CamelJsonModel


class HealthCheck(CamelJsonModel):
    service: str
    version: str
    description: str
