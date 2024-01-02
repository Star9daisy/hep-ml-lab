from functools import reduce

from ..types import Observable


class InvariantMass(Observable):
    def get_value(self):
        for subs in self.sub_objs:
            if len(subs) != 0:
                return

        values = []
        sub_objs = []
        for objs in self.main_objs:
            sub_objs.append(reduce(lambda i, j: i.P4() + j.P4(), objs))

        values.append(reduce(lambda i, j: i.P4() + j.P4(), sub_objs).M())

        return values


class InvMass(InvariantMass):
    ...


class InvM(InvariantMass):
    ...


InvariantMass.add_alias("invariant_mass")
InvMass.add_alias("inv_mass")
InvM.add_alias("inv_m")
