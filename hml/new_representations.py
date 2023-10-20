from __future__ import annotations

import numpy as np
import pandas as pd

from .new_observables import Observable, get_observable


class Set:
    def __init__(self, observables: list[Observable | str]) -> None:
        self.observables = []
        for obs in observables:
            if isinstance(obs, Observable):
                self.observables.append(obs)
            elif isinstance(obs, str):
                self.observables.append(get_observable(obs))
            else:
                raise TypeError(f"Invalid type {type(obs)} for observable {obs}")

        self.names = [obs.name for obs in self.observables]
        self.values = []

    def read(self, event) -> None:
        for obs in self.observables:
            obs.read(event)

        self.values.append([obs.value for obs in self.observables])

    def to_numpy(self, dtype=np.float32) -> np.ndarray:
        return np.array(self.values, dtype=dtype)

    def to_pandas(self) -> pd.DataFrame:
        return pd.DataFrame([self.values], columns=self.names)
