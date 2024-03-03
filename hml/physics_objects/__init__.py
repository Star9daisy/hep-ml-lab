from .collective import Collective, is_collective
from .nested import Nested, is_nested
from .physics_object import ALL_OBJECTS_DICT, PhysicsObject
from .single import Single, is_single


def get(identifier: str | None):
    return ALL_OBJECTS_DICT.get(identifier)


def parse(name: str | None) -> PhysicsObject | None:
    if name is None:
        return

    elif is_single(name):
        return Single.from_name(name)

    elif is_collective(name):
        return Collective.from_name(name)

    elif is_nested(name):
        return Nested.from_name(name)

    else:
        raise ValueError(f"Invalid '{name}' for a physics object")
