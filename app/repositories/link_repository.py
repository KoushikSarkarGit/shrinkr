from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.linkModel import Link


class LinkRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_code(self, code: str) -> Link | None:

        statement = select(Link).where(Link.code == code)
        return await self.session.scalar(statement)

    async def get_active_by_code_for_user(self, code: str, user_id: UUID) -> Link | None:

        statement = select(Link).where(
            Link.code == code,
            Link.user_id == user_id,
            Link.deleted_at.is_(None),
        )
        return await self.session.scalar(statement)

    async def create_link(self, newLink: Link) -> Link | None:
        self.session.add(newLink)
        await self.session.commit()
        await self.session.refresh(newLink)
        return newLink

    async def soft_delete_by_code_for_user(self, code: str, user_id: UUID) -> bool:
        link = await self.get_active_by_code_for_user(code, user_id)

        if link is None:
            return False

        link.deleted_at = datetime.now(timezone.utc)
        await self.session.commit()
        return True
