from __future__ import annotations

import re
from importlib import import_module
from typing import Any

from .collective import CollectivePhysicsObject
from .collective import is_collective_physics_object
from .nested import NestedPhysicsObject
from .nested import is_nested_physics_object
from .physics_object import PhysicsObject
from .physics_object import PhysicsObjectOptions
from .single import SinglePhysicsObject
from .single import is_single_physics_object

PATTERN = r"^([A-Za-z]+\d*:?\d*(?:\.[A-Za-z]+\d*:?\d*)*)$"


def is_multiple_physics_object(
    identifier: str | PhysicsObject | None,
    supported_objects: PhysicsObjectOptions | list[PhysicsObjectOptions] = "all",
) -> bool:
    if identifier is None or identifier == "":
        return False

    if isinstance(identifier, PhysicsObject):
        identifier = identifier.name

    if "," not in identifier:
        return False

    physics_object_names = identifier.split(",")

    if supported_objects == "all":
        for n in physics_object_names:
            if re.match(PATTERN, n) is None:
                return False
        return True
    else:
        for n in physics_object_names:
            status = []
            if "single" in supported_objects:
                status.append(is_single_physics_object(n))
            if "collective" in supported_objects:
                status.append(is_collective_physics_object(n))
            if "nested" in supported_objects:
                status.append(is_nested_physics_object(n))
            if not any(status):
                return False
        return True


class MultiplePhysicsObject(PhysicsObject):
    def __init__(
        self,
        *physics_objects: SinglePhysicsObject | CollectivePhysicsObject,
    ):
        self.all = physics_objects

        self._name = None

    def read(self, event):
        return [obj.read(event) for obj in self.all]

    @property
    def name(self) -> str:
        if self._name is not None:
            return self._name

        return ",".join([obj.name for obj in self.all])

    @classmethod
    def from_name(cls, name: str) -> MultiplePhysicsObject:
        name = name.replace(" ", "")

        if not is_multiple_physics_object(name):
            raise ValueError(
                f"Could not parse name {name} as a multiple physics object"
            )

        physics_object_names = name.split(",")
        physics_objects = []
        for n in physics_object_names:
            if is_single_physics_object(n):
                physics_objects.append(SinglePhysicsObject.from_name(n))
            elif is_collective_physics_object(n):
                physics_objects.append(CollectivePhysicsObject.from_name(n))
            else:
                physics_objects.append(NestedPhysicsObject.from_name(n))

        instance = cls(*physics_objects)
        instance._name = name
        return instance

    @property
    def config(self) -> dict[str, Any]:
        config = {
            "class_name": "MultiplePhysicsObject",
            "all_configs": [obj.config for obj in self.all],
        }
        return config

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> MultiplePhysicsObject:
        if config.get("class_name") != "MultiplePhysicsObject":
            raise ValueError(
                f"Cannot parse config as multiple physics objects: {config}"
            )

        physics_objects = []
        for obj_config in config["all_configs"]:
            module = import_module("hml.physics_objects")
            class_ = getattr(module, obj_config["class_name"])
            physics_objects.append(class_.from_config(obj_config))

        return cls(*physics_objects)
