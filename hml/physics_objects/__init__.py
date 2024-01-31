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


def get_physics_object(name: str | None) -> PhysicsObject | None:
    """Retrieve a physics object from its name.

    Parameters
    ----------
    name : str
        The name of a physics object.

    Returns
    -------
    physics object : PhysicsObject
    """
    if name is None:
        return None

    elif is_single(name):
        obj = Single.from_name(name)

    elif is_collective(name):
        obj = Collective.from_name(name)

    elif is_nested(name):
        obj = Nested.from_name(name)

    elif is_multiple(name):
        obj = Multiple.from_name(name)

    else:
        raise ValueError(f"Unknown physics object {name}")

    return obj
