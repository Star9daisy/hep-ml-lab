from ..types import Observable


class Mass(Observable):
    def get_value(self):
        if len(self.main_objs) != 1:
            return

        values = []
        if len(self.sub_objs[0]) == 0:
            for obj in self.main_objs[0]:
                value = obj.P4().M() if obj is not None else float("nan")
                values.append(value)
        else:
            for main in self.sub_objs[0]:
                for sub in main:
                    value = sub.P4().M() if sub is not None else float("nan")
                    values.append(value)

        return values


class M(Mass):
    ...
