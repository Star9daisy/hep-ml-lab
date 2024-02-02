from math import nan

from ..physics_objects.collective import is_collective
from ..physics_objects.single import is_single
from .observable import Observable


class MomentumX(Observable):
    def __init__(self, physics_object: str):
        supported_types = ["single", "collective", "nested"]
        super().__init__(physics_object, supported_types)

    def read_ttree(self, event):
        objs = self.physics_object.read_ttree(event).objects

        if is_single(self.physics_object.name):
            self._value = objs[0].P4().Px() if objs != [] else nan

        elif is_collective(self.physics_object.name):
            self._value = [obj.P4().Px() if obj is not None else nan for obj in objs]

        else:
            self._value = [
                [sub.P4().Px() if sub is not None else nan for sub in obj]
                for obj in objs
            ]

        return self


class Px(MomentumX):
    ...


MomentumX.add_alias("momentum_x")
Px.add_alias("px")
