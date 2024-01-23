from math import nan
from typing import Any

from ..physics_objects.collective import is_collective
from ..physics_objects.single import is_single
from .observable import Observable


class AzimuthalAngle(Observable):
    def __init__(
        self,
        physics_object: str,
        name: str | None = None,
        value: Any = None,
        dtype: Any = None,
    ):
        supported_types = ["single", "collective", "nested"]
        super().__init__(physics_object, supported_types, name, value, dtype)

    def read(self, event):
        self.physics_object.read(event)

        if is_single(self.physics_object):
            self._value = self.physics_object.objects[0].P4().Phi()

        elif is_collective(self.physics_object):
            self._value = []
            for obj in self.physics_object.objects:
                if obj is not None:
                    self._value.append(obj.P4().Phi())
                else:
                    self._value.append(nan)

        else:
            self._value = []
            for i in self.physics_object.objects:
                values = [j.P4().Phi() if j is not None else nan for j in i]
                self._value.append(values)

        return self


class Phi(AzimuthalAngle):
    ...


AzimuthalAngle.add_alias("azimuthal_angle")
Phi.add_alias("phi")
