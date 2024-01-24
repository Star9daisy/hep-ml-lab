from __future__ import annotations

from math import nan
from typing import Any

from ..physics_objects.single import is_single
from .observable import Observable


class TauTag(Observable):
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
        objs = self.physics_object.objects

        if is_single(self.physics_object):
            self._value = objs[0].TauTag if objs != [] else nan

        else:
            self._value = [obj.TauTag if obj is not None else nan for obj in objs]

        return self


TauTag.add_alias("tau_tag")
