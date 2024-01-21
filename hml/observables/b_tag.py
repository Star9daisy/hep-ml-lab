from math import nan
from typing import Any

from ..physics_objects.physics_object import PhysicsObjectOptions
from ..physics_objects.single import is_single_physics_object
from .observable import Observable


class BTag(Observable):
    def __init__(
        self,
        physics_object: str,
        name: str | None = None,
        supported_objects: list[PhysicsObjectOptions] = ["single", "collective"],
        dtype: Any = None,
    ):
        super().__init__(physics_object, name, supported_objects, dtype)

    def read(self, event):
        if (branch := self.physics_object.read(event)) is None:
            self._value = nan

        elif is_single_physics_object(self.physics_object):
            self._value = branch.BTag

        else:
            self._value = [obj.BTag if obj is not None else nan for obj in branch]

        return self


BTag.add_alias("b_tag")
