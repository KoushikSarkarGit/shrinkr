import uuid
from uuid import UUID

from app.models.linkModel import Link
from app.repositories.link_repository import LinkRepository
from app.schemas.link_schema import LinkCreate
from app.exceptions.link_exceptions import LinkAlreadyExistsError


class LinkService:
    def __init__(self, link_repository: LinkRepository):
        self.link_repository = link_repository

    async def get_link_by_code(self, code: str) -> Link | None:
        return await self.link_repository.get_by_code(code)

    async def create_link(self, linkdata: LinkCreate, user_id: UUID) -> Link:
        nlink = Link(
            user_id=user_id,
            code=linkdata.custom_alias or str(uuid.uuid4()),  # for now
            target_url=str(linkdata.target_url),
        )

        doesexist = await self.link_repository.get_by_code(nlink.code)

        if doesexist:
            raise LinkAlreadyExistsError(nlink.code)

        return await self.link_repository.create_link(nlink)
