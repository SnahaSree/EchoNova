from app.database.connection import mongodb


def create_indexes() -> None:
    users = mongodb.database["users"]

    users.create_index(
        "email",
        unique=True,
        name="unique_user_email",
    )