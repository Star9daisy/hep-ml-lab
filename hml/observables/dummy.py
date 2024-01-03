from ..types import Observable


class Dummy(Observable):
    def get_value(self):
        return [1]
