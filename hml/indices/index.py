from typing import Self, Any

from typeguard import typechecked


@typechecked
class Index:
    PATTERN = r"\d*:?\d*"

    def __eq__(self, other: Any) -> bool:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError

    @property
    def value(self) -> int | slice:
        raise NotImplementedError

    @property
    def name(self) -> str:
        raise NotImplementedError

    @classmethod
    def from_name(cls, name: str) -> Self:
        raise NotImplementedError

    @property
    def config(self) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> Self:
        raise NotImplementedError
