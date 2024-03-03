import re

from .collective import Collective
from .physics_object import PhysicsObject
from .single import Single, is_single


def is_nested(object_: str | PhysicsObject | None) -> bool:
    if object_ is None:
        return False

    elif isinstance(object_, PhysicsObject):
        return isinstance(object_, Nested)

    else:
        return bool(re.match(r"^[a-zA-Z]+\d*:?\d*\.[a-zA-Z]+\d*:?\d*$", object_))


class Nested(PhysicsObject):
    def __init__(
        self,
        main: str | PhysicsObject,
        sub: str | PhysicsObject,
    ) -> None:
        self.main = main
        self.sub = sub

    @classmethod
    def from_name(cls, name: str) -> "Nested":
        main, sub = name.split(".")

        return cls(main, sub)

    @property
    def main(self) -> PhysicsObject:
        return self._main

    @main.setter
    def main(self, main: str | PhysicsObject) -> None:
        if is_single(main):
            self._main = Single.from_name(main) if isinstance(main, str) else main
        else:
            self._main = Collective.from_name(main) if isinstance(main, str) else main

    @property
    def sub(self) -> PhysicsObject:
        return self._sub

    @sub.setter
    def sub(self, sub: str | PhysicsObject) -> None:
        if is_single(sub):
            self._sub = Single.from_name(sub) if isinstance(sub, str) else sub
        else:
            self._sub = Collective.from_name(sub) if isinstance(sub, str) else sub

    @property
    def branch(self) -> str:
        return self.main.branch + "." + self.sub.branch

    @property
    def name(self) -> str:
        return self.main.name + "." + self.sub.name

    @property
    def slices(self) -> list[slice]:
        return [*self.main.slices, *self.sub.slices]

    @property
    def config(self) -> dict:
        return {"main": self.main.name, "sub": self.sub.name}
