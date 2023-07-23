from __future__ import annotations

import cppyy
import numpy as np

from .observables import Observable


class Set:
    """Set represents one event as a set of observables.

    Parameters
    ----------
    observables : list[Observable]
        List of observables.

    Attributes
    ----------
    observables : list[Observable]
        List of observables.
    names : list[str]
        List of names of observables.
    values : np.ndarray
        2D array of values of observables.
    """

    def __init__(self, observables: list[Observable]):
        self.observables = observables
        self.names = [obs.name for obs in observables]
        self.values = None

    def from_event(self, event: cppyy.gbl.TTree):
        """Fill observables from one event.

        Parameters
        ----------
        event : TTree
            One event from a ROOT file.
        """
        for obs in self.observables:
            obs.from_event(event)

        # Stack 1D values of observables into 2D array
        self.values = np.stack([obs.values for obs in self.observables], axis=0)
        self.values = np.squeeze(self.values, axis=1)
