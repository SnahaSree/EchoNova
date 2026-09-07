from app.database.connection import mongodb


def create_indexes() -> None:
    users = mongodb.database["users"]

    users.create_index(
        "email",
        unique=True,
        name="unique_user_email",
    )

    entities = mongodb.database["entities"]

    entities.create_index(
        [
            ("visibility", 1),
            ("created_at", -1),
        ],
        name="entity_visibility_created",
    )

    entities.create_index(
        [
            ("owner_id", 1),
            ("created_at", -1),
        ],
        name="entity_owner_created",
    )

    entities.create_index(
        "entity_type",
        name="entity_type_index",
    )

    entities.create_index(
        "tags",
        name="entity_tags_index",
    )

    entities.create_index(
        [
            ("name", 1),
            ("entity_type", 1),
        ],
        name="entity_name_type",
    )

    relationships = mongodb.database["relationships"]

    relationships.create_index(
        [
            ("source_entity_id", 1),
            ("target_entity_id", 1),
            ("relationship_type", 1),
        ],
        unique=True,
        name="unique_relationship",
    )

    relationships.create_index(
        "source_entity_id",
        name="relationship_source",
    )

    relationships.create_index(
        "target_entity_id",
        name="relationship_target",
    )

    relationships.create_index(
        [
            ("source_entity_id", 1),
            ("target_entity_id", 1),
        ],
        name="relationship_endpoints",
    )