import uuid
from uuid import UUID

from app.exceptions.link_exceptions import LinkAlreadyExistsError, LinkNotFoundError
from app.models.linkModel import Link
from app.repositories.link_repository import LinkRepository
from app.schemas.link_schema import LinkCreate


class LinkService:
    def __init__(self, link_repository: LinkRepository):
        self.link_repository = link_repository

    async def get_link_by_code(self, code: str, user_id: UUID) -> Link:
        link = await self.link_repository.get_active_by_code_for_user(code, user_id)

        if link is None:
            raise LinkNotFoundError(code)

        return link

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

    async def delete_link(self, code: str, user_id: UUID) -> None:
        deleted = await self.link_repository.soft_delete_by_code_for_user(code, user_id)

        if not deleted:
            raise LinkNotFoundError(code)
