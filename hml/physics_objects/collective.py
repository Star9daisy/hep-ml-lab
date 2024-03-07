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
        start: int | None = None,
        stop: int | None = None,
    ) -> None:
        self._branch = branch
        self._start = start
        self._stop = stop

    @property
    def branch(self) -> str:
        return self._branch

    @property
    def start(self) -> int | None:
        return self._start

    @property
    def stop(self) -> int | None:
        return self._stop

    @property
    def slices(self) -> list[slice]:
        return [slice(self.start, self.stop)]

    @property
    def name(self) -> str:
        if self.start is None and self.stop is None:
            return f"{self.branch}"

        elif self.start is None:
            return f"{self.branch}:{self.stop}"

        elif self.stop is None:
            return f"{self.branch}{self.start}:"

        else:
            return f"{self.branch}{self.start}:{self.stop}"

    @classmethod
    def from_name(cls, name: str) -> Collective:
        if re.match(r"^[a-zA-Z]+$|^[a-zA-Z]+\d*:\d*$", name.strip()):
            match_ = re.match(r"^([a-zA-Z]+)(\d*):?(\d*)$", name)
            branch, start, stop = match_.groups()
            start = int(start) if start != "" else None
            stop = int(stop) if stop != "" else None

            return cls(branch, start, stop)

        raise ValueError("Invalid name")

    @property
    def config(self) -> dict:
        return {
            "branch": self.branch,
            "start": self.start,
            "stop": self.stop,
        }
