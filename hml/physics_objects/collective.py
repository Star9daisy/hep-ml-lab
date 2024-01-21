from __future__ import annotations

import re
from typing import Any

from .physics_object import PhysicsObject

PATTERN1 = r"^([A-Za-z]+)$"
PATTERN2 = r"^([A-Za-z]+)(\d+):$"
PATTERN3 = r"^([A-Za-z]+):(\d+)$"
PATTERN4 = r"^([A-Za-z]+)(\d+):(\d+)$"


def is_collective_physics_object(identifier: str | PhysicsObject | None) -> bool:
    if identifier is None or identifier == "":
        return False

    if isinstance(identifier, PhysicsObject):
        identifier = identifier.name

    if re.match(PATTERN1, identifier):
        return True
    elif re.match(PATTERN2, identifier):
        return True
    elif re.match(PATTERN3, identifier):
        return True
    elif re.match(PATTERN4, identifier):
        return True
    else:
        return False


class CollectivePhysicsObject(PhysicsObject):
    def __init__(self, type: str, start: int | None = None, end: int | None = None):
        self.type = type
        self.start = start
        self.end = end

        self._name = None

    def read(self, event):
        if self.type not in [i.GetName() for i in event.GetListOfBranches()]:
            raise ValueError(f"Branch {self.type} not found in event")

        branch = list(getattr(event, self.type))

        if self.start is None and self.end is None:
            return branch

        elif self.start is None:
            objects = branch[: self.end]
            if len(objects) < self.end:
                objects += [None] * (self.end - len(objects))
            return objects

        elif self.end is None:
            return branch[self.start :]

        else:
            objects = branch[self.start : self.end]
            if len(objects) < self.end - self.start:
                objects += [None] * (self.end - self.start - len(objects))
            return objects

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
        name = name.replace(" ", "")

        if m := re.match(PATTERN1, name):
            instance = cls(m.group(1), None, None)

        elif m := re.match(PATTERN2, name):
            instance = cls(m.group(1), int(m.group(2)), None)

        elif m := re.match(PATTERN3, name):
            instance = cls(m.group(1), None, int(m.group(2)))

        elif m := re.match(PATTERN4, name):
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
