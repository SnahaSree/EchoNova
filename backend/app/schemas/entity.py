from datetime import datetime

from pydantic import BaseModel, Field

from app.models.entity import EntityType, EntityVisibility


class EntityCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    entity_type: EntityType
    description: str = Field(default="", max_length=5000)
    visibility: EntityVisibility = EntityVisibility.PRIVATE
    tags: list[str] = Field(default_factory=list)
    image_url: str | None = None


class EntityUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )
    description: str | None = Field(
        default=None,
        max_length=5000,
    )
    visibility: EntityVisibility | None = None
    tags: list[str] | None = None
    image_url: str | None = None


class EntityPublic(BaseModel):
    id: str
    name: str
    entity_type: EntityType
    description: str
    visibility: EntityVisibility
    tags: list[str]
    image_url: str | None
    owner_id: str | None
    created_at: datetime
    updated_at: datetime


class EntityListResponse(BaseModel):
    items: list[EntityPublic]
    page: int
    page_size: int
    total: int
    has_next: bool