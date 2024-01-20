from .collective import CollectivePhysicsObject
from .collective import is_collective_physics_object
from .multiple import MultiplePhysicsObject
from .multiple import is_multiple_physics_object
from .nested import NestedPhysicsObject
from .nested import is_nested_physics_object
from .physics_object import PhysicsObject
from .single import SinglePhysicsObject
from .single import is_single_physics_object


def get(name: str | None):
    if name is None or name == "":
        return None

    if is_single_physics_object(name):
        obj = SinglePhysicsObject.from_name(name)
    elif is_collective_physics_object(name):
        obj = CollectivePhysicsObject.from_name(name)
    elif is_nested_physics_object(name):
        obj = NestedPhysicsObject.from_name(name)
    elif is_multiple_physics_object(name):
        obj = MultiplePhysicsObject.from_name(name)
    else:
        raise ValueError(f"Unknown physics object {name}")

    return obj
