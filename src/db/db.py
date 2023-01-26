from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src import settings

__all__ = ("get_async_session",)

async_engine = create_async_engine(
    settings.postgres.async_dsn,
    echo=True,
    future=True,
)


async def get_async_session() -> AsyncSession:
    async_session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session
