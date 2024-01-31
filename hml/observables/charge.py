from math import nan

from ..physics_objects.single import is_single
from .observable import Observable


class Charge(Observable):
    def __init__(self, physics_object: str):
        supported_types = ["single", "collective"]
        super().__init__(physics_object, supported_types)

    def read_ttree(self, event):
        self.physics_object.read_ttree(event)
        objs = (
            self.physics_object.value
            if isinstance(self.physics_object.value, list)
            else [self.physics_object.value]
        )

        if is_single(self.physics_object.name):
            self._value = objs[0].Charge if objs != [None] else nan

        else:
            self._value = [obj.Charge if obj is not None else nan for obj in objs]

        return self


Charge.add_alias("charge")
