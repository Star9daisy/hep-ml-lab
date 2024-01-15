from ..types import Observable


class Size(Observable):
    def get_value(self):
        if len(self.main_objs) != 1:
            return

        if len(self.sub_objs[0]) != 0:
            return

        values = [len(self.main_objs[0])]

        return values


Size.add_alias("size")
