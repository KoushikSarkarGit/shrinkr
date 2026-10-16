from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_link_service
from app.schemas.link_schema import LinkCreate, LinkResponse
from app.services.link_service import LinkService

router = APIRouter(prefix="/links", tags=["Links"])


@router.get("/{code}", response_model=LinkResponse)
async def get_link(
    code: str,
    user_id: UUID,  # Temporary until authentication is implemented
    link_service: LinkService = Depends(get_link_service),
) -> LinkResponse:
    return await link_service.get_link_by_code(code=code, user_id=user_id)


@router.post(
    "",
    response_model=LinkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_link(
    link_data: LinkCreate,
    user_id: UUID,  # Temporary until authentication is implemented
    link_service: LinkService = Depends(get_link_service),
) -> LinkResponse:
    return await link_service.create_link(link_data, user_id)


@router.delete(
    "/delete/{code}",
    response_model=LinkResponse,
    status_code=status.HTTP_301_MOVED_PERMANENTLY,
)
async def delete_link(
    code: str,
    user_id: UUID,  # Temporary until authentication is implemented
    link_service: LinkService = Depends(get_link_service),
) -> LinkResponse:
    return await link_service.delete_link(code, user_id)
