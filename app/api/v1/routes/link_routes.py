from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_link_service
from app.schemas.link_schema import LinkCreate, LinkResponse
from app.services.link_service import LinkService

router = APIRouter(prefix="/links", tags=["Links"])


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
