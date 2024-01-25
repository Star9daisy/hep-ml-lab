from .collective import Collective
from .collective import is_collective
from .multiple import Multiple
from .multiple import is_multiple
from .nested import Nested
from .nested import is_nested
from .physics_object import PhysicsObject
from .single import Single
from .single import is_single

ALL_OBJECTS_DICT = {
    "single": Single,
    "collective": Collective,
    "nested": Nested,
    "multiple": Multiple,
}


def get(identifier: str) -> PhysicsObject:
    """Retrieve a physics object from an identifier.

    Parameters
    ----------
    identifier : str
        A unique string for a physics object.

    Returns
    -------
    physics object : PhysicsObject
    """
    if is_single(identifier):
        obj = Single.from_id(identifier)

    elif is_collective(identifier):
        obj = Collective.from_id(identifier)

    elif is_nested(identifier):
        obj = Nested.from_id(identifier)

    elif is_multiple(identifier):
        obj = Multiple.from_id(identifier)

    else:
        raise ValueError(f"Unknown physics object {identifier}")

    return obj
