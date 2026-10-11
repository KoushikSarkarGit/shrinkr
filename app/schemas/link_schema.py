from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class LinkCreate(BaseModel):
    target_url: HttpUrl
    custom_alias: str | None = Field(default=None, max_length=50)


class LinkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    code: str
    target_url: str
    created_at: datetime
