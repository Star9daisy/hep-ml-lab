from __future__ import annotations

import re
from importlib import import_module
from typing import Any

from .collective import CollectivePhysicsObject
from .single import SinglePhysicsObject
from .single import is_single_physics_object


def is_nested_physics_object(name: str) -> bool:
    return bool(re.match(NestedPhysicsObject.pattern, name))


class NestedPhysicsObject:
    pattern = r"^([A-Za-z]+\d*:?\d*).([A-Za-z]+\d*:?\d*)$"

    def __init__(
        self,
        main: SinglePhysicsObject | CollectivePhysicsObject,
        sub: SinglePhysicsObject | CollectivePhysicsObject,
    ):
        self.main = main
        self.sub = sub

        self._name = None

    @property
    def name(self) -> str:
        if self._name is not None:
            return self._name

        return f"{self.main.name}.{self.sub.name}"

    @classmethod
    def from_name(cls, name: str) -> NestedPhysicsObject:
        if (match := re.match(cls.pattern, name)) is None:
            raise ValueError(f"Could not parse name {name} as a nested physics object")

        # main --------------------------------------------------------------- #
        main_match = match.group(1)
        if is_single_physics_object(main_match):
            main = SinglePhysicsObject.from_name(main_match)
        else:
            main = CollectivePhysicsObject.from_name(main_match)

        # sub ---------------------------------------------------------------- #
        sub_match = match.group(2)
        if is_single_physics_object(sub_match):
            sub = SinglePhysicsObject.from_name(sub_match)
        else:
            sub = CollectivePhysicsObject.from_name(sub_match)

        instance = cls(main, sub)
        instance._name = name
        return instance

    @property
    def config(self) -> dict[str, Any]:
        config = {
            "class_name": "NestedPhysicsObject",
            "main_config": self.main.config,
            "sub_config": self.sub.config,
        }
        return config

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> NestedPhysicsObject:
        if config.get("class_name") != "NestedPhysicsObject":
            raise ValueError(f"Cannot parse config as NestedPhysicsObject: {config}")

        # main --------------------------------------------------------------- #
        main_class_name = config["main_config"]["class_name"]
        main = getattr(
            import_module("hml.physics_objects"), main_class_name
        ).from_config(config["main_config"])

        # sub ---------------------------------------------------------------- #
        sub_class_name = config["sub_config"]["class_name"]
        sub = getattr(import_module("hml.physics_objects"), sub_class_name).from_config(
            config["sub_config"]
        )

        return cls(main, sub)
