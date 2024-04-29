from __future__ import annotations

import re

from .angular_distance import AngularDistance
from .charge import Charge
from .invariant_mass import InvariantMass
from .kinematics import E, Eta, M, Phi, Pt, Px, Py, Pz
from .n_subjettiness import NSubjettiness, NSubjettinessRatio, TauMN, TauN
from .observable import Observable
from .size import Size
from .tag import BTag, TauTag


def get(identifier: str | None) -> Observable | None:
    if identifier is None or identifier == "None":
        return

    else:
        return Observable.aliases.get(identifier)


def register_observable(obs: Observable, *alias: str) -> None:
    for name in alias:
        Observable.aliases[name] = obs


def parse_observable(name: str | None, **kwargs) -> Observable | None:
    if name is None or (isinstance(name, str) and name == "None"):
        return

    if (class_name := name.split(".")[-1]) in Observable.aliases:
        kwargs["class_name"] = class_name
        return Observable.aliases[class_name].from_name(name, **kwargs)

    elif re.match(r"^tau\d$", class_name.lower()):
        kwargs["class_name"] = class_name
        return TauN.from_name(name, **kwargs)

    elif re.match(r"^tau\d\d$", class_name.lower()):
        kwargs["class_name"] = class_name
        return TauMN.from_name(name, **kwargs)

    else:
        raise ValueError(f"Invalid '{name}' for an observable")
