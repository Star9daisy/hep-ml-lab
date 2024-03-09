from __future__ import annotations

import re

from .physics_object import PhysicsObject


def is_single(object_: PhysicsObject | str) -> bool:
    """Check if an object is a single physics object"""
    if isinstance(object_, PhysicsObject):
        return isinstance(object_, Single)

    return bool(re.match(r"^[a-zA-Z]+\d+$", object_))


class Single(PhysicsObject):
    """A single physics object"""

    def __init__(self, branch: str, index: int) -> None:
        self._branch = branch
        self._index = index

    @classmethod
    def from_name(cls, name: str) -> Single:
        if match_ := re.match(r"^([a-zA-Z]+)(\d+)$", name.strip()):
            branch, index = match_.groups()
            return cls(branch, int(index))

        raise ValueError(f"Invalid name '{name}' for a single physics object")

    @property
    def index(self) -> int:
        return self._index

    @property
    def branch(self) -> str:
        return self._branch

    @property
    def slices(self) -> list[slice]:
        return [slice(self.index, self.index + 1)]

    @property
    def name(self) -> str:
        return f"{self.branch}{self.index}"

    @property
    def config(self) -> dict:
        return {"branch": self.branch, "index": self.index}
