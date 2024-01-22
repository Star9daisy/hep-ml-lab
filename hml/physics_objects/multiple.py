from __future__ import annotations

from typing import Any

from .physics_object import PhysicsObject
from .collective import Collective
from .collective import is_collective
from .nested import Nested
from .nested import is_nested
from .single import Single
from .single import is_single


def is_multiple(identifier: str) -> bool:
    try:
        Multiple.from_identifier(identifier)
        return True
    except Exception:
        return False


class Multiple(PhysicsObject):
    def __init__(self, *physics_objects: Single | Collective | Nested):
        self.all = physics_objects
        self.objects = []

    def read(self, source: Any):
        self.objects = [obj.read(source).objects for obj in self.all]
        return self

    @property
    def identifier(self) -> str:
        return ",".join([obj.identifier for obj in self.all])

    @classmethod
    def from_identifier(cls, identifier: str) -> Multiple:
        if "," not in identifier:
            raise ValueError(f"Invalid identifier {identifier} for {cls.__name__}")

        objects = []
        for i in identifier.split(","):
            if is_single(i):
                objects.append(Single.from_identifier(i))
            elif is_collective(i):
                objects.append(Collective.from_identifier(i))
            elif is_nested(i):
                objects.append(Nested.from_identifier(i))
            else:
                raise ValueError(f"Invalid identifier {identifier} for {cls.__name__}")
        return cls(*objects)

    @property
    def config(self) -> dict[str, Any]:
        return {"classname": "Multiple", "configs": [obj.config for obj in self.all]}

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> Multiple:
        if config.get("classname") != "Multiple":
            raise ValueError(f"Invalid config for {cls.__name__}")

        objects = []
        for obj in config.get("configs"):
            if obj.get("classname") == "Single":
                objects.append(Single.from_config(obj))
            elif obj.get("classname") == "Collective":
                objects.append(Collective.from_config(obj))
            elif obj.get("classname") == "Nested":
                objects.append(Nested.from_config(obj))
            else:
                raise ValueError(f"Invalid config for {cls.__name__}")
        return cls(*objects)

    def __eq__(self, other: Multiple) -> bool:
        for obj1, obj2 in zip(self.all, other.all):
            if obj1 != obj2:
                return False
        return True

    def __repr__(self):
        return self.identifier
