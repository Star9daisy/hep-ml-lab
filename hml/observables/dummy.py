import random

from ..types import Observable


class Dummy(Observable):
    def get_value(self):
        return [random.random()]
