from .collective import Collective, is_collective
from .multiple import Multiple, is_multiple
from .nested import Nested, is_nested
from .physics_object import PhysicsObject
from .single import Single, is_single

ALL_OBJECTS = {Single, Collective, Nested, Multiple}
ALL_OBJECTS_DICT = {cls.__name__: cls for cls in ALL_OBJECTS}
ALL_OBJECTS_DICT.update({cls.__name__.lower(): cls for cls in ALL_OBJECTS})


def get(identifier: str | None) -> PhysicsObject | None:
    if identifier is None or identifier == "None":
        return

    else:
        return ALL_OBJECTS_DICT.get(identifier)


def parse(name: str | PhysicsObject | None) -> PhysicsObject | None:
    if name is None or (isinstance(name, str) and name == "None"):
        return

    elif isinstance(name, PhysicsObject):
        return name

    elif is_single(name):
        return Single.from_name(name)

    elif is_collective(name):
        return Collective.from_name(name)

    elif is_nested(name):
        return Nested.from_name(name)

    elif is_multiple(name):
        return Multiple.from_name(name)

    else:
        raise ValueError(f"Invalid '{name}' for a physics object")
