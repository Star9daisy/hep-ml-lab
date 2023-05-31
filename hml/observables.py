from __future__ import annotations
import re
import numpy as np
from ROOT import TLorentzVector


def separate_text_and_number(s):
    if "+" in s:
        s = s.split("+")
        names, indices = [], []
        for name, index in [separate_text_and_number(part) for part in s]:
            names.append(name)
            indices.append(index)

        return names, indices

    match = re.match(r"([a-z]+)([0-9]+)", s, re.I)
    if match:
        items = match.groups()
        items = (items[0], int(items[1]))
    else:
        raise ValueError(
            f"{s} should be in the form of object and index like Jet0, Muon1..."
        )
    return items


class Observable:
    pass


class PT(Observable):
    def __init__(self, name: str, value: float | None = None):
        self.name = name
        self.value = value
        self.obs_name = f"{name}_PT"

    def from_event(self, event):
        if "+" in self.name:
            _branch_names, _indices = separate_text_and_number(self.name)
            combined_object = TLorentzVector()
            for _branch_name, _index in zip(_branch_names, _indices):
                _branch = getattr(event, _branch_name)
                n_objects = _branch.GetEntries()
                if _index >= n_objects:
                    raise IndexError(
                        f"Index {_index} is out of range in branch {_branch_name}"
                    )
                combined_object += _branch[_index].P4()

            self.value = combined_object.Pt()
        else:
            _branch_name, _index = separate_text_and_number(self.name)
            _branch = getattr(event, _branch_name)
            n_objects = _branch.GetEntries()
            if _index >= n_objects:
                raise IndexError(f"Index {_index} is out of range in branch {_branch}")
            else:
                self.value = _branch[_index].PT
