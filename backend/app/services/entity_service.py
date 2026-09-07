from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.models.entity import EntityVisibility
from app.repositories.entity_repository import entity_repository
from app.schemas.entity import EntityCreate, EntityUpdate


class EntityService:
    def create(
        self,
        data: EntityCreate,
        owner_id: str,
    ) -> str:
        now = datetime.now(timezone.utc)

        document = {
            "name": data.name.strip(),
            "entity_type": data.entity_type.value,
            "description": data.description.strip(),
            "visibility": data.visibility.value,
            "tags": [
                tag.strip()
                for tag in data.tags
                if tag.strip()
            ],
            "image_url": data.image_url,
            "owner_id": owner_id,
            "created_at": now,
            "updated_at": now,
        }

        return entity_repository.create(document)

    def get(
        self,
        entity_id: str,
        current_user_id: str,
    ) -> dict:
        entity = entity_repository.find_by_id(entity_id)

        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entity not found.",
            )

        is_public = (
            entity["visibility"]
            == EntityVisibility.PUBLIC.value
        )

        is_owner = (
            entity.get("owner_id")
            == current_user_id
        )

        if not is_public and not is_owner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entity not found.",
            )

        return entity

    def update(
        self,
        entity_id: str,
        data: EntityUpdate,
        current_user_id: str,
    ) -> dict:
        entity = entity_repository.find_by_id(entity_id)

        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entity not found.",
            )

        if entity.get("owner_id") != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to modify this entity.",
            )

        updates = data.model_dump(
            exclude_unset=True,
        )

        if "name" in updates and updates["name"]:
            updates["name"] = updates["name"].strip()

        if "description" in updates and updates["description"]:
            updates["description"] = updates["description"].strip()

        if "visibility" in updates:
            updates["visibility"] = updates[
                "visibility"
            ].value

        if "tags" in updates:
            updates["tags"] = [
                tag.strip()
                for tag in updates["tags"]
                if tag.strip()
            ]

        updated = entity_repository.update(
            entity_id,
            updates,
        )

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entity not found.",
            )

        return updated

    def delete(
        self,
        entity_id: str,
        current_user_id: str,
    ) -> None:
        entity = entity_repository.find_by_id(entity_id)

        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entity not found.",
            )

        if entity.get("owner_id") != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this entity.",
            )

        deleted = entity_repository.delete(entity_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entity not found.",
            )

    def list(
        self,
        current_user_id: str,
        page: int,
        page_size: int,
        entity_type: str | None = None,
    ) -> dict:
        skip = (page - 1) * page_size

        entities = entity_repository.list_entities(
            skip=skip,
            limit=page_size,
            current_user_id=current_user_id,
            entity_type=entity_type,
        )

        total = entity_repository.count(
            current_user_id=current_user_id,
            entity_type=entity_type,
        )

        return {
            "items": entities,
            "page": page,
            "page_size": page_size,
            "total": total,
            "has_next": page * page_size < total,
        }


entity_service = EntityService()