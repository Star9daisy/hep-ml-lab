from math import nan
from typing import Any

from ..physics_objects.collective import is_collective
from ..physics_objects.single import is_single
from .observable import Observable


class TransverseMomentum(Observable):
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
        objs = self.physics_object.objects

        if is_single(self.physics_object):
            self._value = objs[0].P4().Pt() if objs != [] else nan

        elif is_collective(self.physics_object):
            self._value = [obj.P4().Pt() if obj is not None else nan for obj in objs]

        else:
            self._value = [
                [sub.P4().Pt() if sub is not None else nan for sub in obj]
                for obj in objs
            ]

        return self


class Pt(TransverseMomentum):
    ...


TransverseMomentum.add_alias("transverse_momentum")
Pt.add_alias("pt", "pT", "PT")
