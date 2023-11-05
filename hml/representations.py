from __future__ import annotations

import numpy as np
import pandas as pd

from .observables import Observable, get_observable


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

    def __init__(self, observables: list[Observable | str]) -> None:
        self.observables = []
        for obs in observables:
            if isinstance(obs, Observable):
                self.observables.append(obs)
            else:
                self.observables.append(get_observable(obs))

        self.names = [obs.name for obs in self.observables]
        self.values = []

    def read_event(self, event) -> None:
        for obs in self.observables:
            obs.read_event(event)

        self.values.append([obs.value for obs in self.observables])

    def to_numpy(self, dtype=np.float32) -> np.ndarray:
        return np.array(self.values, dtype=dtype)

    def to_pandas(self) -> pd.DataFrame:
        return pd.DataFrame(self.values, columns=self.names)
