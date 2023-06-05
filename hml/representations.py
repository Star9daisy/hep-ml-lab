from __future__ import annotations

import numpy as np

from .observables import Observable


class Set:
    def __init__(self, observables: list[Observable]):
        self.observables = observables

    @property
    def values(self):
        return np.array(self._values)

    def from_event(self, event):
        self._values = []
        for obs in self.observables:
            obs.from_event(event)
            self._values.append(obs.values)
