import re

from .physics_object import PhysicsObject


def is_collective(object_: str | PhysicsObject | None) -> bool:
    if object_ is None:
        return False

    elif isinstance(object_, PhysicsObject):
        return isinstance(object_, Collective)

    else:
        return bool(re.match(r"^[a-zA-Z]+$|^[a-zA-Z]+\d*:\d*$", object_))


class Collective(PhysicsObject):
    def __init__(
        self,
        branch: str,
        start: int | None = None,
        stop: int | None = None,
    ) -> None:
        self.branch = branch
        self.start = start
        self.stop = stop

    @classmethod
    def from_name(cls, name: str) -> "Collective":
        if re.match(r"^[a-zA-Z]+$|^[a-zA-Z]+\d*:\d*$", name) is None:
            raise ValueError(
                f"Invalid name '{name}' for a {cls.__name__} physics object"
            )

        match_ = re.match(r"^([a-zA-Z]+)(\d*):?(\d*)$", name)
        branch, start, stop = match_.groups()
        start = int(start) if start != "" else None
        stop = int(stop) if stop != "" else None

        return cls(branch, start, stop)

    @property
    def branch(self) -> str:
        return self._branch

    @branch.setter
    def branch(self, branch: str) -> None:
        self._branch = branch

    @property
    def start(self) -> int:
        return self._start

    @start.setter
    def start(self, start: None | int) -> None:
        self._start = start

    @property
    def stop(self) -> int:
        return self._stop

    @stop.setter
    def stop(self, stop: None | int) -> None:
        self._stop = stop

    @property
    def name(self) -> str:
        match self.start, self.stop:
            case None, None:
                return f"{self.branch}"
            case None, _:
                return f"{self.branch}:{self.stop}"
            case _, None:
                return f"{self.branch}{self.start}:"
            case _:
                return f"{self.branch}{self.start}:{self.stop}"

    @property
    def slices(self) -> list[slice]:
        return [slice(self.start, self.stop)]

    @property
    def config(self) -> dict:
        return {"branch": self.branch, "start": self.start, "stop": self.stop}
