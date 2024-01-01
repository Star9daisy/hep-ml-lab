from ..types import Observable


class Size(Observable):
    def get_value(self):
        if len(self.main_phyobjs) != 1:
            return

        if len(self.sub_phyobjs[0]) != 0:
            return

        return len(self.main_phyobjs[0])
