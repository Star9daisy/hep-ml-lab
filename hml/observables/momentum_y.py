from math import nan
from typing import Any

from ..physics_objects.collective import is_collective_physics_object
from ..physics_objects.physics_object import PhysicsObjectOptions
from ..physics_objects.single import is_single_physics_object
from .observable import Observable


class MomentumY(Observable):
    def __init__(
        self,
        physics_object: str,
        name: str | None = None,
        supported_objects: list[PhysicsObjectOptions] = [
            "single",
            "collective",
            "nested",
        ],
        dtype: Any = None,
    ):
        super().__init__(physics_object, name, supported_objects, dtype)

    def read(self, event):
        if (branch := self.physics_object.read(event)) is None:
            self._value = nan

        elif is_single_physics_object(self.physics_object):
            self._value = branch.P4().Py()

        elif is_collective_physics_object(self.physics_object):
            self._value = [obj.P4().Py() if obj is not None else nan for obj in branch]

        else:
            self._value = []
            for main in branch:
                sub_values = [sub.P4().Py() if sub is not None else nan for sub in main]
                self._value.append(sub_values)

        return self


class Py(MomentumY):
    ...


MomentumY.add_alias("momentum_y")
Py.add_alias("py")
