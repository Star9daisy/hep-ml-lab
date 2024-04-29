from __future__ import annotations

from importlib import import_module

import awkward as ak

from hml.observables import Observable, parse_observable


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

    def __init__(self, observables: list[str | Observable]):
        self.observables = self._init_observables(observables)
        self._values = None

    def _init_observables(self, observables: list[str | Observable]):
        output = []
        for obs in observables:
            if isinstance(obs, str):
                output.append(parse_observable(obs))
            else:
                output.append(obs)

        return output

    def read(self, events):
        values = []
        for obs in self.observables:
            obs.read(events)

            if len(obs.shape) == 2:
                # Maybe a single or collective observable
                if obs.shape[-1] != "1":
                    raise ValueError

                value = obs.value

            if len(obs.shape) == 3:
                # Should be the delta_r observable
                if obs.shape[1] == "1" and obs.shape[2] == "1":
                    value = obs.value[:, :, 0]

            values.append(value)

        self._values = ak.concatenate(values, axis=1)

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
                i: {
                    "class_name": obs.__class__.__name__,
                    "config": obs.config,
                }
                for i, obs in enumerate(self.observables)
            },
        }

    @classmethod
    def from_config(cls, config):
        observables = []

        for i_config in config["observable_configs"].values():
            class_type = Observable.aliases[i_config["class_name"]]
            class_name = class_type.__name__
            module = import_module(class_type.__module__)
            class_ = getattr(module, class_name)
            class_config = i_config["config"]
            observables.append(class_.from_config(class_config))

        return cls(observables)
