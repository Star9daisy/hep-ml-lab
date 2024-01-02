from ..types import Observable


class NSubjettinessRatio(Observable):
    def __init__(self, physics_object, m, n):
        super().__init__(physics_object)
        self.m = m
        self.n = n

    def get_value(self):
        if len(self.main_objs) != 1:
            return

        if len(self.sub_objs[0]) != 0:
            return

        values = []
        for obj in self.main_objs[0]:
            if obj is None:
                value = float("nan")
            elif obj.Tau[self.n - 1] == 0:
                value = float("nan")
            else:
                value = obj.Tau[self.m - 1] / obj.Tau[self.n - 1]
            values.append(value)

        return values


class TauMN(NSubjettinessRatio):
    ...


NSubjettinessRatio.add_alias("n_subjettiness_ratio")
TauMN.add_alias("tau_mn")
