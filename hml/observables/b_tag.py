from ..types import Observable


class BTag(Observable):
    def get_value(self):
        if len(self.main_objs) != 1:
            return

        if len(self.sub_objs[0]) != 0:
            return

        values = []
        for obj in self.main_objs[0]:
            value = obj.BTag if obj is not None else float("nan")
            values.append(value)

        return values


BTag.add_alias("b_tag")
