from math import nan

from ..physics_objects.collective import is_collective
from ..physics_objects.single import is_single
from .observable import Observable


class PseudoRapidity(Observable):
    def __init__(self, physics_object: str):
        supported_types = ["single", "collective", "nested"]
        super().__init__(physics_object, supported_types)

    def read_ttree(self, event):
        self.physics_object.read_ttree(event)
        objs = (
            self.physics_object.value
            if isinstance(self.physics_object.value, list)
            else [self.physics_object.value]
        )

        if is_single(self.physics_object.name):
            self._value = objs[0].P4().Eta() if objs != [None] else nan

        elif is_collective(self.physics_object.name):
            self._value = [obj.P4().Eta() if obj is not None else nan for obj in objs]

        else:
            self._value = [
                [sub.P4().Eta() if sub is not None else nan for sub in obj]
                for obj in objs
            ]

        return self


class Eta(PseudoRapidity):
    ...


PseudoRapidity.add_alias("pseudo_rapidity")
Eta.add_alias("eta")
