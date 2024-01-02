from ..types import Observable


class NSubjettiness(Observable):
    def __init__(self, physics_object, n):
        super().__init__(physics_object)
        self.n = n

    def get_value(self):
        if len(self.main_objs) != 1:
            return

        if len(self.sub_objs[0]) != 0:
            return

        values = []
        for obj in self.main_objs[0]:
            value = obj.Tau[self.n - 1] if obj is not None else float("nan")
            values.append(value)

        return values


class TauN(NSubjettiness):
    ...


NSubjettiness.add_alias("n_subjettiness")
TauN.add_alias("tau_n")
