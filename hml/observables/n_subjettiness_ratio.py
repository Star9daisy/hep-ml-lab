from ..types import Observable


class NSubjettinessRatio(Observable):
    def __init__(self, name, m, n):
        super().__init__(name)
        self.m = m
        self.n = n

    def get_value(self):
        if len(self.main_phyobjs) != 1:
            return

        if len(self.sub_phyobjs[0]) != 0:
            return

        values = []
        for obj in self.main_phyobjs[0]:
            if obj is None:
                values.append(float("nan"))
            elif obj.Tau[self.n - 1] == 0:
                values.append(float("nan"))
            else:
                values.append(obj.Tau[self.m - 1] / obj.Tau[self.n - 1])

        return values


class TauMN(NSubjettinessRatio):
    ...
