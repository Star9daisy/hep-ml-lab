import re

from .physics_object import PhysicsObject


def is_single(object_: str | PhysicsObject | None) -> bool:
    if object_ is None:
        return False

    elif isinstance(object_, PhysicsObject):
        return isinstance(object_, Single)

    else:
        return bool(re.match(r"^[a-zA-Z]+\d+$", object_))


class Single(PhysicsObject):
    def __init__(self, branch: str, index: int) -> None:
        self.branch = branch
        self.index = index

    @classmethod
    def from_name(cls, name: str) -> "Single":
        if (match_ := re.match(r"^([a-zA-Z]+)(\d+)$", name)) is None:
            raise ValueError(
                f"Invalid name '{name}' for a {cls.__name__} physics object"
            )

        branch, index = match_.groups()

        return cls(branch, int(index))

    @property
    def branch(self) -> str:
        return self._branch

    @branch.setter
    def branch(self, branch: str) -> None:
        self._branch = branch

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, index: int) -> None:
        self._index = int(index)

    @property
    def name(self) -> str:
        return self.branch + str(self.index)

    @property
    def slices(self) -> list[slice]:
        return [slice(self.index, self.index + 1)]

    @property
    def config(self) -> dict:
        return {"branch": self.branch, "index": self.index}


Single.add_alias("single")
