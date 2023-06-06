from __future__ import annotations

import numpy as np

from .observables import Observable


class Set:
    def __init__(self, observables: list[Observable]):
        self.observables = observables
        self.names = [obs.name for obs in observables]
        self.values = None

    def from_event(self, event):
        for obs in self.observables:
            obs.from_event(event)

        # Stack 1D values of observables into 2D array
        self.values = np.stack([obs.values for obs in self.observables], axis=0)
        self.values = np.squeeze(self.values, axis=1)
