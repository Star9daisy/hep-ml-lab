from __future__ import annotations

import awkward as ak

from hml.physics_objects.physics_object import PhysicsObject

from .observable import Observable


class NSubjettiness(Observable):
    def __init__(
        self,
        n: int,
        physics_object: str | PhysicsObject,
        class_name: str | None = None,
    ) -> None:
        supported_objects = ["single", "collective"]
        super().__init__(physics_object, class_name, supported_objects)
        self.n = n

    def read(self, events):
        all_keys = {i.lower(): i for i in events.keys(full_paths=False)}
        branch = self.physics_object.branch.lower()
        slices = self.physics_object.slices

        if f"{branch}.tau[5]" in all_keys:
            key = all_keys[f"{branch}.tau[5]"]
            array = events[key].array()[:, slices[0]]
            value = array[:, :, self.n - 1]

        else:
            raise ValueError

        for i, slice_ in enumerate(slices):
            if slice_.stop is not None:
                start = slice_.start if slice_.start is not None else 0
                required_length = slice_.stop - start

                if i + 1 == len(slices) and ak.any(
                    ak.num(value, i + 1) < required_length
                ):
                    value = ak.pad_none(value, required_length, axis=i + 1)

                else:
                    n_missing = required_length - ak.num(value, i + 1)
                    if ak.sum(n_missing) > 0:
                        pad = ak.unflatten(
                            ak.Array([[]] * ak.sum(n_missing)), n_missing
                        )
                        value = ak.concatenate([value, pad], axis=i + 1)

        self._value = value

        return self

    @property
    def config(self):
        config = super().config
        config.update({"n": self.n})
        return config


NSubjettiness.with_aliases("n_subjettiness")


class TauN(NSubjettiness):
    @classmethod
    def from_name(cls, name: str, **kwargs) -> TauN:
        *parts, class_name = name.split(".")
        physics_object = ".".join(parts) if len(parts) > 0 else None

        if class_name.lower().startswith("tau"):
            if "n" not in kwargs:
                n = int(class_name[-1])
            else:
                n = kwargs["n"]

        return cls(n, physics_object, class_name)


TauN.with_aliases("tau_n")


class NSubjettinessRatio(Observable):
    def __init__(
        self,
        m: int,
        n: int,
        physics_object: str | PhysicsObject,
        class_name: str | None = None,
    ) -> None:
        supported_objects = ["single", "collective"]
        super().__init__(physics_object, class_name, supported_objects)
        self.m = m
        self.n = n

        self.tau_m = TauN(m, physics_object)
        self.tau_n = TauN(n, physics_object)

    def read(self, events):
        self.tau_m.read(events)
        self.tau_n.read(events)

        self._value = self.tau_m.value / self.tau_n.value

        return self

    @property
    def config(self):
        config = super().config
        config.update({"m": self.m, "n": self.n})
        return config


NSubjettinessRatio.with_aliases("n_subjettiness_ratio")


class TauMN(NSubjettinessRatio):
    @classmethod
    def from_name(cls, name: str, **kwargs) -> TauMN:
        *parts, class_name = name.split(".")
        physics_object = ".".join(parts) if len(parts) > 0 else None

        if class_name.lower().startswith("tau"):
            if "m" not in kwargs:
                m = int(class_name[-2])
            else:
                m = kwargs["m"]

            if "n" not in kwargs:
                n = int(class_name[-1])
            else:
                n = kwargs["n"]

        return cls(m, n, physics_object, class_name)


TauMN.with_aliases("tau_mn")
