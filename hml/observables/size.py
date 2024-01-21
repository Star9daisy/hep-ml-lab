from typing import Any

from ..physics_objects.physics_object import PhysicsObjectOptions
from .observable import Observable


class Size(Observable):
    def __init__(
        self,
        physics_object: str,
        name: str | None = None,
        supported_objects: list[PhysicsObjectOptions] = ["collective"],
        dtype: Any = None,
    ):
        super().__init__(physics_object, name, supported_objects, dtype)

    def read(self, event):
        branch = self.physics_object.read(event)
        self._value = len(branch)

        return self


Size.add_alias("size")
