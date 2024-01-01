from ..types import Observable


class NSubjettiness(Observable):
    def __init__(self, name, n):
        super().__init__(name)
        self.n = n

    def get_value(self):
        if len(self.main_phyobjs) != 1:
            return

        if len(self.sub_phyobjs[0]) != 0:
            return

        values = [
            obj.Tau[self.n - 1] if obj is not None else float("nan")
            for obj in self.main_phyobjs[0]
        ]
        return values


class TauN(NSubjettiness):
    ...
