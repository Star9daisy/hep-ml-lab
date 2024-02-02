from importlib import import_module

import numpy as np

from hml.observables import Observable
from hml.observables import get_observable


class Set:
    """A set of observables.

    Set is a 1D representation of an event. It contains a list of observables.
    It is usually used as input to approaches like CutAndCount and
    ToyMultilayerPerceptron (MLP).

    Parameters
    ----------
    *observables : list[Observable | str]
        A list of observables or their names.
    """

    def __init__(self, *observables: str | Observable):
        self.observables = []
        for obs in observables:
            if isinstance(obs, str):
                obs = get_observable(obs)

            self.observables.append(obs)

        self._values = None

    def read_ttree(self, event):
        self._values = []

        for obs in self.observables:
            value = obs.read_ttree(event).to_numpy()

            # Check if the observable is a scalar
            if value.shape != ():
                raise ValueError(
                    f"Observable {obs.name} has shape {obs.to_numpy().shape} "
                    "but should be a scalar."
                )

            self._values.append(value)

        self._values = np.array(self._values)

        return self

    @property
    def names(self):
        return [i.name for i in self.observables]

    @property
    def values(self):
        return self._values

    @property
    def config(self):
        return {
            "observable_configs": {
                i.__class__.__name__: i.config for i in self.observables
            },
        }

    @classmethod
    def from_config(cls, config):
        observables = []
        module = import_module("hml.observables")

        for class_name, class_config in config["observable_configs"].items():
            class_ = getattr(module, class_name)
            observables.append(class_.from_config(class_config))

        return cls(*observables)
