from __future__ import annotations

from .collective import Collective, is_collective
from .nested import Nested
from .physics_object import PhysicsObject
from .single import Single, is_single


def is_multiple(
    object_: PhysicsObject | str,
    supported_types: list[PhysicsObject | str] | None = None,
) -> bool:
    """Check if an object is a multiple physics object"""
    if isinstance(object_, str):
        try:
            object_ = Multiple.from_name(object_)
        except Exception:
            return False

    if supported_types is None:
        return True

    supported_types = [
        i.lower() if isinstance(i, str) else i.__class__.__name__.lower()
        for i in supported_types
    ]

    for obj in object_.all:
        if obj.__class__.__name__.lower() not in supported_types:
            return False

    return True


class Multiple(PhysicsObject):
    """A multiple physics object"""

    def __init__(self, all: list[PhysicsObject | str]) -> None:
        self._all = self._init_all(all)

    def _init_all(self, objects: list[PhysicsObject | str]) -> list[PhysicsObject]:
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

    @classmethod
    def from_name(cls, name: str) -> Multiple:
        if "," in name:
            all_ = name.split(",")
            return cls(all_)

        raise ValueError(f"Invalid name '{name}' for a multiple physics object")

    @property
    def all(self) -> list[PhysicsObject]:
        return self._all

    @property
    def branch(self) -> list[str]:
        return [obj.branch for obj in self.all]

    @property
    def slices(self) -> list[list[slice]]:
        return [i.slices for i in self.all]

    @property
    def name(self) -> str:
        return ",".join(obj.name for obj in self.all)

    @property
    def config(self) -> dict:
        return {"all": [i.name for i in self.all]}
