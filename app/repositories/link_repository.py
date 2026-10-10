from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.linkModel import Link


class LinkRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_code(self, code: str) -> Link | None:
        statement = select(Link).where(Link.code == code)
        return await self.session.scalar(statement)
