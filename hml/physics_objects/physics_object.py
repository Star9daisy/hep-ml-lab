from abc import ABC
from abc import abstractclassmethod
from abc import abstractmethod
from abc import abstractproperty
from typing import Any


class PhysicsObject(ABC):
    @abstractmethod
    def read(self, event):
        ...

    @abstractproperty
    def name(self):
        ...

    @abstractclassmethod
    def from_name(cls, name: str):
        ...

    @abstractproperty
    def config(self) -> dict[str, Any]:
        ...

    @abstractclassmethod
    def from_config(cls, config: dict[str, Any]):
        ...
