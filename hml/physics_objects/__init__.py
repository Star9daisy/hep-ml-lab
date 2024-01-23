from .collective import Collective
from .collective import is_collective
from .multiple import Multiple
from .multiple import is_multiple
from .nested import Nested
from .nested import is_nested
from .physics_object import PhysicsObject
from .single import Single
from .single import is_single


def get(classname: str) -> PhysicsObject:
    """Retrieve a physics object class from a name.

    Parameters
    ----------
    classname : str
        A unique string for a physics object class.

    Returns
    -------
    physics object : PhysicsObject
    """
    name = classname.lower()

    if name == "single":
        return Single

    elif name == "collective":
        return Collective

    elif name == "nested":
        return Nested

    elif name == "multiple":
        return Multiple

    else:
        raise ValueError(f"Unknown physics object type {classname}")
