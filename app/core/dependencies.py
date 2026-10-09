from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, settings
from app.infrastructure.database.database import AsyncSessionLocal


def get_settings() -> Settings:
    return settings


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    # async with ensures the session is closed when its context exits, including when an exception occurs.
    async with AsyncSessionLocal as session:
        yield session
