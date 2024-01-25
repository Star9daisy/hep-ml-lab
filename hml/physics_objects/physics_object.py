from __future__ import annotations

from abc import ABC
from abc import abstractclassmethod
from abc import abstractmethod
from abc import abstractproperty
from typing import Any


class PhysicsObject(ABC):
    @abstractmethod
    def read_ttree(self, ttree):
        ...

    @abstractproperty
    def id(self):
        ...

    @abstractclassmethod
    def from_id(cls, id: str):
        ...

    @abstractproperty
    def config(self) -> dict[str, Any]:
        ...

    @abstractclassmethod
    def from_config(cls, config: dict[str, Any]):
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.id}"

    def __eq__(self, other: PhysicsObject) -> bool:
        return self.config == other.config
