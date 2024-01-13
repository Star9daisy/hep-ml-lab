import numpy as np

from hml.types import Observable
from hml.utils import get_observable


class Set:
    """A set of observables.

    Set is a 1D representation of an event. It contains a list of observables.
    It is usually used as input to approaches like CutAndCount and
    ToyMultilayerPerceptron (MLP).

    Parameters
    ----------
    observables : list[Observable | str]
        A list of observables or their names.
    """

    def __init__(self, *observables: str | Observable):
        self.observables = []
        for i in observables:
            if isinstance(i, str):
                self.observables.append(get_observable(i))
            else:
                self.observables.append(i)

        self.values = None

    def read(self, event):
        for i in self.observables:
            i.read(event)

        self.values = self.get_values()

    def get_values(self):
        values = []

        for i in self.observables:
            values += i.value

        return values

    def to_numpy(self, dtype="float32"):
        return np.array(self.values, dtype=dtype)
