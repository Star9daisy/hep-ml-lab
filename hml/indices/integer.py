import re
from typing import Any, Self

from typeguard import typechecked

from .index import Index


@typechecked
class IntegerIndex(Index):
    PATTERN = r"(?P<number>\d+)"

    def __init__(self, number: int = 0) -> None:
        self.number = number

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, IntegerIndex):
            return False

        return self.number == other.number

    def __repr__(self) -> str:
        return f"IntegerIndex(number={self.number})"

    @property
    def value(self) -> int:
        return self.number

    @classmethod
    def from_int(cls, int_: int) -> Self:
        return cls(number=int_)

    @property
    def name(self) -> str:
        return str(self.number)

    @classmethod
    def from_name(cls, name: str) -> Self:
        if (match := re.fullmatch(cls.PATTERN, name)) is None:
            raise ValueError(
                f"Invalid name pattern for IntegerIndex."
                f"Received: {name=} while expecting: {cls.PATTERN=}"
            )

        group = match.groupdict()
        number = int(group["number"])

        return cls(number=number)

    @property
    def config(self) -> dict[str, Any]:
        return {"number": self.number}

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> Self:
        if "number" not in config:
            raise ValueError(f"Required 'number' in config. Received: {config=}")

        number = config["number"]

        return cls(number=number)
