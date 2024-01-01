from ..types import Observable


class Charge(Observable):
    def get_value(self):
        if len(self.main_phyobjs) != 1:
            return

        if len(self.sub_phyobjs[0]) != 0:
            return

        values = [
            obj.Charge if obj is not None else float("nan")
            for obj in self.main_phyobjs[0]
        ]
        return values
