from enum import Enum


class EntityType(str, Enum):
    CONCEPT = "concept"
    PERSON = "person"
    PLACE = "place"
    EVENT = "event"
    TECHNOLOGY = "technology"
    SCIENTIFIC_TERM = "scientific_term"
    OBJECT = "object"
    ORGANIZATION = "organization"
    WORK = "work"
    SPECIES = "species"


class EntityVisibility(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"