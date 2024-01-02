from functools import reduce

from ..types import Observable


class InvariantMass(Observable):
    def get_value(self):
        for subs in self.sub_objs:
            if len(subs) != 0:
                return

        values = []
        flat_objs = []
        for objs in self.main_objs:
            for obj in objs:
                flat_objs.append(obj)
        self.flat_objs = flat_objs

        value = flat_objs[0].P4()
        for obj in flat_objs[1:]:
            value = value + obj.P4()
        values.append(value.M())

        return values


class InvMass(InvariantMass):
    ...


class InvM(InvariantMass):
    ...


InvariantMass.add_alias("invariant_mass")
InvMass.add_alias("inv_mass")
InvM.add_alias("inv_m")
