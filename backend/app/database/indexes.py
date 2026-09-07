from app.database.connection import mongodb


def create_indexes() -> None:
    # =========================
    # Users
    # =========================
    users = mongodb.database["users"]

    users.create_index(
        "email",
        unique=True,
        name="unique_user_email",
    )

    # =========================
    # Entities
    # =========================
    entities = mongodb.database["entities"]

    # Visibility + newest first
    entities.create_index(
        [
            ("visibility", 1),
            ("created_at", -1),
        ],
        name="entity_visibility_created",
    )

    # Owner + newest first
    entities.create_index(
        [
            ("owner_id", 1),
            ("created_at", -1),
        ],
        name="entity_owner_created",
    )

    # Entity type
    entities.create_index(
        "entity_type",
        name="entity_type_index",
    )

    # Entity type + newest first
    entities.create_index(
        [
            ("entity_type", 1),
            ("created_at", -1),
        ],
        name="entity_type_created",
    )

    # Tags
    entities.create_index(
        "tags",
        name="entity_tags_index",
    )

    # Entity name
    entities.create_index(
        "name",
        name="entity_name",
    )

    # Name + entity type
    entities.create_index(
        [
            ("name", 1),
            ("entity_type", 1),
        ],
        name="entity_name_type",
    )

    # =========================
    # Relationships
    # =========================
    relationships = mongodb.database["relationships"]

    # Prevent duplicate relationships
    relationships.create_index(
        [
            ("source_entity_id", 1),
            ("target_entity_id", 1),
            ("relationship_type", 1),
        ],
        unique=True,
        name="unique_relationship",
    )

    # Source entity lookup
    relationships.create_index(
        "source_entity_id",
        name="relationship_source",
    )

    # Target entity lookup
    relationships.create_index(
        "target_entity_id",
        name="relationship_target",
    )

    # Endpoint lookup
    relationships.create_index(
        [
            ("source_entity_id", 1),
            ("target_entity_id", 1),
        ],
        name="relationship_endpoints",
    )
