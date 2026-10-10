from app.models.linkModel import Link
from app.repositories.link_repository import LinkRepository


class LinkService:
    def __init__(self, link_repository: LinkRepository):
        self.link_repository = link_repository

    async def get_link_by_code(self, code: str) -> Link | None:
        return await self.link_repository.get_by_code(code)
