from __future__ import annotations

import re
from typing import Any


def is_collective_physics_object(name: str) -> bool:
    if re.match(CollectivePhysicsObject.pattern1, name):
        return True
    elif re.match(CollectivePhysicsObject.pattern2, name):
        return True
    elif re.match(CollectivePhysicsObject.pattern3, name):
        return True
    elif re.match(CollectivePhysicsObject.pattern4, name):
        return True
    else:
        return False


class CollectivePhysicsObject:
    pattern1 = r"^([A-Za-z]+)$"
    pattern2 = r"^([A-Za-z]+)(\d+):$"
    pattern3 = r"^([A-Za-z]+):(\d+)$"
    pattern4 = r"^([A-Za-z]+)(\d+):(\d+)$"

    def __init__(self, type: str, start: int | None = None, end: int | None = None):
        self.type = type
        self.start = start
        self.end = end

        self._name = None

    @property
    def name(self) -> str:
        if self._name is not None:
            return self._name

        elif self.start is None and self.end is None:
            return self.type

        else:
            start_str = "" if self.start is None else str(self.start)
            end_str = "" if self.end is None else str(self.end)
            return f"{self.type}{start_str}:{end_str}"

    @classmethod
    def from_name(cls, name: str) -> CollectivePhysicsObject:
        if m := re.match(cls.pattern1, name):
            instance = cls(m.group(1), None, None)

        elif m := re.match(cls.pattern2, name):
            instance = cls(m.group(1), int(m.group(2)), None)

        elif m := re.match(cls.pattern3, name):
            instance = cls(m.group(1), None, int(m.group(2)))

        elif m := re.match(cls.pattern4, name):
            instance = cls(m.group(1), int(m.group(2)), int(m.group(3)))

        else:
            raise ValueError(f"Could not parse name {name}")

        instance._name = name
        return instance

    @property
    def config(self) -> dict[str, Any]:
        config = {
            "class_name": "CollectivePhysicsObject",
            "type": self.type,
            "start": self.start,
            "end": self.end,
        }
        return config

    @classmethod
    def from_config(cls, config) -> CollectivePhysicsObject:
        if config.get("class_name") != "CollectivePhysicsObject":
            raise ValueError(
                f"Cannot parse config as CollectivePhysicsObject: {config}"
            )

        return cls(config["type"], config["start"], config["end"])
