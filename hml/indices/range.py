import re
from typing import Any, Self

from typeguard import typechecked

from .index import Index


@typechecked
class RangeIndex(Index):
    PATTERN = r"(?:(?P<start>\d+)?:(?P<stop>\d+)?)?"

    def __init__(self, start: int | None = None, stop: int | None = None) -> None:
        self.start = start
        self.stop = stop

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, RangeIndex):
            return False

        return self.start == other.start and self.stop == other.stop

    def __repr__(self) -> str:
        return f"RangeIndex(start={self.start}, stop={self.stop})"

    @property
    def value(self) -> slice:
        return slice(self.start, self.stop)

    @classmethod
    def from_slice(cls, slice_: slice) -> Self:
        return cls(start=slice_.start, stop=slice_.stop)

    @property
    def name(self) -> str:
        if self.start is None and self.stop is None:
            return ""
        elif self.start is None:
            return f":{self.stop}"
        elif self.stop is None:
            return f"{self.start}:"
        else:
            return f"{self.start}:{self.stop}"

    @classmethod
    def from_name(cls, name: str) -> Self:
        if (match := re.fullmatch(cls.PATTERN, name)) is None:
            raise ValueError(
                f"Invalid name pattern for RangeIndex. "
                f"Received: {name=} while expecting: {cls.PATTERN=}"
            )

        group = match.groupdict()
        start, stop = group["start"], group["stop"]
        start = int(start) if start is not None else None
        stop = int(stop) if stop is not None else None

        return cls(start=start, stop=stop)

    @property
    def config(self) -> dict[str, Any]:
        return {"start": self.start, "stop": self.stop}

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> Self:
        if "start" not in config or "stop" not in config:
            raise ValueError(
                f"Required 'start' and 'stop' in config. Received: {config=}"
            )

        start = config["start"]
        stop = config["stop"]

        return cls(start=start, stop=stop)
