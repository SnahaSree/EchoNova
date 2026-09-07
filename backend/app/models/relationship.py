from enum import Enum


class RelationshipType(str, Enum):
    RELATED_TO = "related_to"
    PART_OF = "part_of"
    CREATED_BY = "created_by"
    DISCOVERED_BY = "discovered_by"
    LOCATED_IN = "located_in"
    CAUSES = "causes"
    DEPENDS_ON = "depends_on"
    SIMILAR_TO = "similar_to"
    PRECEDES = "precedes"
    USED_BY = "used_by"
    BORN_IN = "born_in"
    WORKS_FOR = "works_for"
    MEMBER_OF = "member_of"