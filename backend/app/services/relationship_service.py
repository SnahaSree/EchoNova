from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.repositories.entity_repository import entity_repository
from app.repositories.relationship_repository import (
    relationship_repository,
)
from app.schemas.relationship import RelationshipCreate


class RelationshipService:
    def create(
        self,
        data: RelationshipCreate,
        current_user_id: str,
    ) -> dict:
        if (
            data.source_entity_id
            == data.target_entity_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An entity cannot have a relationship with itself.",
            )

        source = entity_repository.find_by_id(
            data.source_entity_id
        )

        target = entity_repository.find_by_id(
            data.target_entity_id
        )

        if not source or not target:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or more entities were not found.",
            )

        self._check_entity_access(
            source,
            current_user_id,
        )

        self._check_entity_access(
            target,
            current_user_id,
        )

        existing = (
            relationship_repository.find_existing(
                source_entity_id=data.source_entity_id,
                target_entity_id=data.target_entity_id,
                relationship_type=data.relationship_type.value,
            )
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This relationship already exists.",
            )

        now = datetime.now(timezone.utc)

        document = {
            "source_entity_id": data.source_entity_id,
            "target_entity_id": data.target_entity_id,
            "relationship_type": (
                data.relationship_type.value
            ),
            "description": data.description.strip(),
            "strength": data.strength,
            "created_by": current_user_id,
            "created_at": now,
            "updated_at": now,
        }

        relationship_id = (
            relationship_repository.create(
                document
            )
        )

        relationship = (
            relationship_repository.find_by_id(
                relationship_id
            )
        )

        if not relationship:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create relationship.",
            )

        return relationship

    def get_related(
        self,
        entity_id: str,
        current_user_id: str,
    ) -> list[dict]:
        entity = entity_repository.find_by_id(
            entity_id
        )

        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entity not found.",
            )

        self._check_entity_access(
            entity,
            current_user_id,
        )

        relationships = (
            relationship_repository.find_related(
                entity_id
            )
        )

        accessible_relationships = []

        for relationship in relationships:
            source = entity_repository.find_by_id(
                relationship["source_entity_id"]
            )

            target = entity_repository.find_by_id(
                relationship["target_entity_id"]
            )

            if not source or not target:
                continue

            try:
                self._check_entity_access(
                    source,
                    current_user_id,
                )

                self._check_entity_access(
                    target,
                    current_user_id,
                )
            except HTTPException:
                continue

            accessible_relationships.append(
                relationship
            )

        return accessible_relationships

    def delete(
        self,
        relationship_id: str,
        current_user_id: str,
    ) -> None:
        relationship = (
            relationship_repository.find_by_id(
                relationship_id
            )
        )

        if not relationship:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relationship not found.",
            )

        if (
            relationship.get("created_by")
            != current_user_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this relationship.",
            )

        deleted = relationship_repository.delete(
            relationship_id
        )

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relationship not found.",
            )

    @staticmethod
    def _check_entity_access(
        entity: dict,
        current_user_id: str,
    ) -> None:
        is_public = (
            entity.get("visibility") == "public"
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


relationship_service = RelationshipService()