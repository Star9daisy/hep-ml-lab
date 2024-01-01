from __future__ import annotations

import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Union

import awkward as ak
import numpy as np

PathLike = Union[str, Path]


class Generator:
    ...


class Observable(ABC):
    def __init__(self, name):
        self._name = name
        self.main_phyobjs = []
        self.sub_phyobjs = []
        self.infos = self.parse_physics_object(self.name)

    def read(self, event):
        for info in self.infos:
            main_branch = info["main"][0]
            main_start = info["main"][1]
            main_end = info["main"][2]
            main_phyobjs = list(getattr(event, main_branch))[
                slice(main_start, main_end)
            ]
            if (main_end is not None) and (len(main_phyobjs) < main_end - main_start):
                main_phyobjs += [None] * (main_end - main_start - len(main_phyobjs))
            self.main_phyobjs.append(main_phyobjs)

            if (sub_info := info.get("sub")) is not None:
                sub_branch = sub_info[0]
                sub_start = sub_info[1]
                sub_end = sub_info[2]

                current_sub_phyobjs = []
                for i in main_phyobjs:
                    if i is None:
                        if sub_end is None:
                            current_sub_phyobjs.append([None])
                        else:
                            current_sub_phyobjs.append([None] * (sub_end - sub_start))
                        continue

                    sub_phyobjs = list(getattr(i, sub_branch))[
                        slice(sub_start, sub_end)
                    ]
                    if (sub_end is int) and (len(sub_phyobjs) < sub_end - sub_start):
                        sub_phyobjs += [None] * (sub_end - sub_start - len(sub_phyobjs))
                    current_sub_phyobjs.append(sub_phyobjs)
                self.sub_phyobjs.append(current_sub_phyobjs)
            else:
                self.sub_phyobjs.append([])

        self._value = self.get_value()

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @property
    def shape(self):
        return self.to_awkward().type.show()

    def to_awkward(self, dtype="float32"):
        ak_array = ak.from_iter(self.value)
        ak_array = ak.values_astype(ak_array, dtype)
        try:
            ak_array = ak.to_regular(ak_array)
        except ValueError:
            pass
        return ak_array

    def to_numpy(self, dtype="float32"):
        return np.array(self._value, dtype=dtype)

    @abstractmethod
    def get_value(self) -> Any:
        ...

    def parse_branch(self, branch: str):
        if re.match(r"^([A-Za-z]+)$", branch):
            branch += ":"

        if match := re.match(r"^([A-Za-z]+)(\d+)$", branch):
            obj, index = match.groups()
            start = int(index)
            stop = start + 1
        elif match := re.match(r"^([A-Za-z]+)(\d*:?\d*)$", branch):
            obj, agnostic_index = match.groups()
            indices = agnostic_index.split(":")
            if indices[0] == "" and indices[1] == "":
                start = 0
                stop = None
            elif indices[0] == "" and indices[1] != "":
                start = 0
                stop = int(indices[1])
            elif indices[0] != "" and indices[1] == "":
                start = int(indices[0])
                stop = None
            else:
                start = int(indices[0])
                stop = int(indices[1])
        else:
            return

        return obj, start, stop

    def parse_physics_object(self, physics_object: str):
        output = []
        for phyobj_name in physics_object.split(","):
            item = {}

            if "." not in phyobj_name:
                item["main"] = self.parse_branch(phyobj_name)
                output.append(item)
            else:
                main, sub = phyobj_name.split(".")
                item["main"] = self.parse_branch(main)
                item["sub"] = self.parse_branch(sub)
                output.append(item)
        return output


class Representation:
    ...


class Dataset:
    ...


class Approach:
    ...


class Metric:
    ...
