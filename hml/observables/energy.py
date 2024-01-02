from ..types import Observable


class Energy(Observable):
    def get_value(self):
        if len(self.main_objs) != 1:
            return

        values = []
        if len(self.sub_objs[0]) == 0:
            for obj in self.main_objs[0]:
                value = obj.P4().E() if obj is not None else float("nan")
                values.append(value)
        else:
            for main in self.sub_objs[0]:
                values_per_main = []
                for sub in main:
                    value = sub.P4().E() if sub is not None else float("nan")
                    values_per_main.append(value)
                values.append(values_per_main)

        return values


class E(Energy):
    ...
