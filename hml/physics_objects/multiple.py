from __future__ import annotations

from .collective import Collective, is_collective
from .nested import Nested
from .physics_object import PhysicsObject
from .single import Single, is_single


def is_multiple(
    object_: str | PhysicsObject | None,
    supported_objects: list[str | PhysicsObject] | None = None,
) -> bool:
    if object_ is None:
        return False

    if isinstance(object_, str):
        try:
            object_ = Multiple.from_name(object_)
        except Exception:
            return False

    elif not isinstance(object_, Multiple):
        return False

    if supported_objects is None:
        return True

    supported_objects = [i if isinstance(i, str) else i.name for i in supported_objects]
    supported_objects = [i.lower() for i in supported_objects]

    for obj in object_.all:
        if obj.__class__.__name__.lower() not in supported_objects:
            return False

    return True


class Multiple(PhysicsObject):
    def __init__(self, objects: list[str | PhysicsObject]) -> None:
        self._all = self._init_all(objects)

    def _init_all(self, objects: list[str | PhysicsObject]) -> list[PhysicsObject]:
        output = []
        for obj in objects:
            if isinstance(obj, PhysicsObject):
                output.append(obj)

            elif is_single(obj):
                output.append(Single.from_name(obj))

            elif is_collective(obj):
                output.append(Collective.from_name(obj))

            else:
                output.append(Nested.from_name(obj))
        return output

    @property
    def all(self) -> list[PhysicsObject]:
        return self._all

    @property
    def branch(self) -> list[str]:
        return [obj.branch for obj in self.all]

    @property
    def slices(self) -> list[list[slice]]:
        return [i.slice for i in all]

    @property
    def name(self) -> str:
        return ",".join(obj.name for obj in self.all)

    @classmethod
    def from_name(cls, name: str) -> Multiple:
        if "," in name:
            all_ = name.split(",")
            return cls(all_)

        raise ValueError

    @property
    def config(self) -> dict:
        return {"objects": [i.name for i in self.all]}
