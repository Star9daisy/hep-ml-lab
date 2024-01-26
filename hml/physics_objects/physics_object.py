from __future__ import annotations

from abc import ABC
from abc import abstractclassmethod
from abc import abstractmethod


class PhysicsObject(ABC):
    @abstractmethod
    def read_ttree(self, ttree):
        ...

    @abstractclassmethod
    def from_name(cls, name: str) -> PhysicsObject:
        ...
