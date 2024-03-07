from __future__ import annotations

import re

from .collective import Collective
from .physics_object import PhysicsObject
from .single import Single, is_single


def is_nested(object_: str | PhysicsObject | None) -> bool:
    if isinstance(object_, str):
        return bool(re.match(r"^[a-zA-Z]+\d*:?\d*\.[a-zA-Z]+\d*:?\d*$", object_))

    elif isinstance(object_, PhysicsObject):
        return isinstance(object_, Nested)

    else:
        return False


class Nested(PhysicsObject):
    def __init__(
        self,
        main: str | PhysicsObject,
        sub: str | PhysicsObject,
    ) -> None:
        self._main = self._init_object(main)
        self._sub = self._init_object(sub)

    def _init_object(self, object_: str | PhysicsObject) -> PhysicsObject:
        if isinstance(object_, PhysicsObject):
            return object_

        elif is_single(object_):
            return Single.from_name(object_)

        else:
            return Collective.from_name(object_)

    @property
    def main(self) -> PhysicsObject:
        return self._main

    @property
    def sub(self) -> PhysicsObject:
        return self._sub

    @property
    def branch(self) -> str:
        return f"{self.main.branch}.{self.sub.branch}"

    @property
    def slices(self) -> list[slice]:
        return [*self.main.slices, *self.sub.slices]

    @property
    def name(self) -> str:
        return f"{self.main.name}.{self.sub.name}"

    @classmethod
    def from_name(cls, name: str) -> Nested:
        if "." in name:
            main, sub = name.split(".")
            return cls(main, sub)

        raise ValueError

    @property
    def config(self) -> dict:
        return {"main": self.main.name, "sub": self.sub.name}
