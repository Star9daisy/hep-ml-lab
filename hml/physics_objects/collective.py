from __future__ import annotations

import re

from .physics_object import PhysicsObject


def is_collective(object_: str | PhysicsObject | None) -> bool:
    if isinstance(object_, str):
        return bool(re.match(r"^[a-zA-Z]+$|^[a-zA-Z]+\d*:\d*$", object_))

    elif isinstance(object_, PhysicsObject):
        return isinstance(object_, Collective)

    else:
        return False


class Collective(PhysicsObject):
    def __init__(
        self,
        branch: str,
        index: tuple[int | None, int | None] = (None, None),
    ) -> None:
        self.branch = branch
        self.index = index

    @property
    def branch(self) -> str:
        return self._branch

    @branch.setter
    def branch(self, branch: str) -> None:
        self._branch = branch

    @property
    def index(self) -> slice:
        return self._index

    @index.setter
    def index(self, index: tuple[int | None, int | None]) -> None:
        self._index = slice(*index)

    @property
    def name(self) -> str:
        if self.index.start is None and self.index.stop is None:
            return f"{self.branch}"

        elif self.index.start is None:
            return f"{self.branch}:{self.index.stop}"

        elif self.index.stop is None:
            return f"{self.branch}{self.index.start}:"

        else:
            return f"{self.branch}{self.index.start}:{self.index.stop}"

    @classmethod
    def from_name(cls, name: str) -> Collective:
        if re.match(r"^[a-zA-Z]+$|^[a-zA-Z]+\d*:\d*$", name.strip()):
            match_ = re.match(r"^([a-zA-Z]+)(\d*):?(\d*)$", name)
            branch, start, stop = match_.groups()
            start = int(start) if start != "" else None
            stop = int(stop) if stop != "" else None

            return cls(branch, (start, stop))

        else:
            raise ValueError

    @property
    def config(self) -> dict:
        return {
            "branch": self.branch,
            "index": (self.index.start, self.index.stop),
        }
