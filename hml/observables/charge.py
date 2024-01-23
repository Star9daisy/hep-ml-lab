from math import nan
from typing import Any

from ..physics_objects.single import is_single
from .observable import Observable


class Charge(Observable):
    def __init__(
        self,
        physics_object: str,
        name: str | None = None,
        value: Any = None,
        dtype: Any = None,
    ):
        supported_types = ["single", "collective"]
        super().__init__(physics_object, supported_types, name, value, dtype)

    def read(self, event):
        self.physics_object.read(event)

        if is_single(self.physics_object):
            obj = self.physics_object.objects[0]
            self._value = obj.Charge if obj else nan

        else:
            self._value = []
            for obj in self.physics_object.objects:
                if obj:
                    self._value.append(obj.Charge)
                else:
                    self._value.append(nan)

        return self


Charge.add_alias("charge")
