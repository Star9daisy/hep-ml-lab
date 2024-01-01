from ..types import Observable


class TransverseMomentum(Observable):
    def get_value(self):
        if len(self.main_phyobjs) != 1:
            return

        main_phyobjs = self.main_phyobjs[0]
        sub_phyobjs = self.sub_phyobjs[0]

        if len(sub_phyobjs) == 0:
            values = [
                obj.P4().Pt() if obj is not None else float("nan")
                for obj in main_phyobjs
            ]
        else:
            values = [
                [sub.P4().Pt() if sub is not None else float("nan") for sub in main]
                for main in self.sub_phyobjs[0]
            ]
        return values


class Pt(TransverseMomentum):
    ...
