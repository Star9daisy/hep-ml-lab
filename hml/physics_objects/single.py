from __future__ import annotations

import re
from typing import Any


class SinglePhysicsObject:
    pattern = r"^([A-Za-z]+)(\d+)$"

    def __init__(self, type: str, index: int):
        self.type = type
        self.index = index

    @property
    def name(self) -> str:
        return f"{self.type}{self.index}"

    @classmethod
    def from_name(cls, name: str) -> SinglePhysicsObject:
        match = re.match(cls.pattern, name)
        type = match.group(1)
        index = int(match.group(2))
        return cls(type, index)

    @property
    def config(self) -> dict[str, Any]:
        config = {
            "single_physics_object_type": self.type,
            "single_physics_object_index": self.index,
        }
        return config

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> SinglePhysicsObject:
        return cls(
            config["single_physics_object_type"],
            config["single_physics_object_index"],
        )
