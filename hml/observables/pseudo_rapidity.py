from math import nan
from typing import Any

from ..physics_objects.collective import is_collective
from ..physics_objects.single import is_single
from .observable import Observable


class PseudoRapidity(Observable):
    def __init__(
        self,
        physics_object: str,
        name: str | None = None,
        dtype: Any = None,
    ):
        supported_types = ["single", "collective", "nested"]
        super().__init__(physics_object, supported_types, name, dtype)

    def read(self, event):
        self.physics_object.read(event)

        if is_single(self.physics_object):
            self._value = self.physics_object.objects[0].P4().Eta()

        elif is_collective(self.physics_object):
            self._value = []
            for obj in self.physics_object.objects:
                if obj is not None:
                    self._value.append(obj.P4().Eta())
                else:
                    self._value.append(nan)

        else:
            self._value = []
            for i in self.physics_object.objects:
                values = [j.P4().Eta() if j is not None else nan for j in i]
                self._value.append(values)

        return self


class Eta(PseudoRapidity):
    ...


PseudoRapidity.add_alias("pseudo_rapidity")
Eta.add_alias("eta")
