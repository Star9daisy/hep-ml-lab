from .observable import Observable


class Dummy(Observable):
    def read_ttree(self, event):
        self._value = 1
        return self


Dummy.add_alias("dummy")
