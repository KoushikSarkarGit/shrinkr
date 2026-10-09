from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# This creates SQLAlchemy's async engine. this engine Manages DB connectivity/poo
engine = create_async_engine(settings.database_url, echo=settings.debug)

# This is a factory for creating AsyncSession objects. Creates database sessions
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass
