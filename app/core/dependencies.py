from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, settings
from app.infrastructure.database.database import AsyncSessionLocal
from app.repositories.link_repository import LinkRepository
from app.repositories.user_repository import UserRepository
from app.services.link_service import LinkService
from app.services.user_service import UserService


def get_settings() -> Settings:
    return settings


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    # async with ensures the session is closed when its context exits, including when an exception occurs.
    async with AsyncSessionLocal() as session:
        yield session


def get_user_repository(
    session: AsyncSession = Depends(get_db),
) -> UserRepository:
    return UserRepository(session)


def get_link_repository(
    session: AsyncSession = Depends(get_db),
) -> LinkRepository:
    return LinkRepository(session)


def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repository)


def get_link_service(
    repository: LinkRepository = Depends(get_link_repository),
) -> LinkService:
    return LinkService(repository)
