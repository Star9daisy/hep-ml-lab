from __future__ import annotations

import re
from importlib import import_module
from typing import Any

from .collective import CollectivePhysicsObject
from .collective import is_collective_physics_object
from .nested import NestedPhysicsObject
from .nested import is_nested_physics_object
from .single import SinglePhysicsObject
from .single import is_single_physics_object


def is_multiple_physics_object(name: str) -> bool:
    if "," not in name:
        return False
    else:
        for n in name.split(","):
            if not (
                is_single_physics_object(n)
                or is_collective_physics_object(n)
                or is_nested_physics_object(n)
            ):
                return False

        return True


class MultiplePhysicsObject:
    def __init__(
        self,
        *physics_objects: SinglePhysicsObject | CollectivePhysicsObject,
    ):
        self.all = physics_objects

        self._name = None

    @property
    def name(self) -> str:
        if self._name is not None:
            return self._name

        return ",".join([obj.name for obj in self.all])

    @classmethod
    def from_name(cls, name: str) -> MultiplePhysicsObject:
        if is_multiple_physics_object(name) is False:
            raise ValueError(
                f"Could not parse name {name} as a multiple physics object"
            )

        physics_objects = []
        for n in name.split(","):
            if is_single_physics_object(n):
                physics_objects.append(SinglePhysicsObject.from_name(n))
            elif is_collective_physics_object(n):
                physics_objects.append(CollectivePhysicsObject.from_name(n))
            elif is_nested_physics_object(n):
                physics_objects.append(NestedPhysicsObject.from_name(n))
            else:
                raise ValueError(f"Could not parse name {name} as a physics object")

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
