import numpy as np
import pandas as pd

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

        self._values = None

    def read(self, event):
        self._values = []

        for i in self.observables:
            value = i.read(event).to_numpy()

            # Check if the observable is a scalar
            if value.shape != ():
                raise ValueError(
                    f"Observable {i.name} has shape {value.shape} "
                    "but should be a scalar."
                )

            self._values.append(value)

        self._values = np.array(self._values)

    @property
    def names(self):
        return [i.name for i in self.observables]

    @property
    def values(self):
        return self._values

    def to_pandas(self):
        return pd.DataFrame(self.values, columns=self.names)
