from __future__ import annotations
from .observables import Observable
import numpy as np


class Set:
    def __init__(self, observables: list[Observable]):
        self.observables = observables
        self.obs_names = [obs.obs_name for obs in observables]
        self._values = []

    @property
    def values(self):
        return np.array(self._values)

    def from_event(self, event):
        for obs in self.observables:
            obs.from_event(event)
            self._values.append(obs.value)
