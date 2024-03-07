from __future__ import annotations

import re

from .physics_object import PhysicsObject


def is_single(object_: str | PhysicsObject | None) -> bool:
    if isinstance(object_, str):
        return bool(re.match(r"^[a-zA-Z]+\d+$", object_))

    elif isinstance(object_, PhysicsObject):
        return isinstance(object_, Single)

    else:
        return False


class Single(PhysicsObject):
    def __init__(self, branch: str, index: int) -> None:
        self._branch = branch
        self._index = index

    @property
    def branch(self) -> str:
        return self._branch

    @property
    def index(self) -> int:
        return self._index

    @property
    def slices(self) -> list[slice]:
        return [slice(self.index, self.index + 1)]

    @property
    def name(self) -> str:
        return f"{self.branch}{self.index}"

    @classmethod
    def from_name(cls, name: str) -> Single:
        if match_ := re.match(r"^([a-zA-Z]+)(\d+)$", name.strip()):
            branch, index = match_.groups()
            return cls(branch, int(index))

        raise ValueError("Invalid name")

    @property
    def config(self) -> dict:
        return {"branch": self.branch, "index": self.index}
