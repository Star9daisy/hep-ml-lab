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

ALL_OBJECTS = {
    Px,
    Py,
    Pz,
    E,
    Pt,
    Eta,
    Phi,
    M,
    Charge,
    BTag,
    TauTag,
    Size,
    NSubjettiness,
    NSubjettinessRatio,
    TauMN,
    TauN,
    InvariantMass,
    AngularDistance,
}
ALL_OBJECTS_DICT = {obj.__name__: obj for obj in ALL_OBJECTS}
ALL_OBJECTS_DICT.update({obj.__name__.lower(): obj for obj in ALL_OBJECTS})
ALL_OBJECTS_DICT.update(
    {
        "MomentumX": Px,
        "momentum_x": Px,
        "MomentumY": Py,
        "momentum_y": Py,
        "MomentumZ": Pz,
        "momentum_z": Pz,
        "Energy": E,
        "energy": E,
        "TransverseMomentum": Pt,
        "transverse_momentum": Pt,
        "PT": Pt,
        "met": Pt,
        "MET": Pt,
        "PseudoRapidity": Eta,
        "pseudo_rapidity": Eta,
        "AzimuthalAngle": Phi,
        "azimuthal_angle": Phi,
        "Mass": M,
        "mass": M,
        "b_tag": BTag,
        "tau_tag": TauTag,
        "n_subjettiness": NSubjettiness,
        "n_subjettiness_ratio": NSubjettinessRatio,
        "tau_mn": TauMN,
        "tau_n": TauN,
        "invariant_mass": InvariantMass,
        "InvMass": InvariantMass,
        "inv_mass": InvariantMass,
        "InvM": InvariantMass,
        "inv_m": InvariantMass,
        "angular_distance": AngularDistance,
        "DeltaR": AngularDistance,
        "delta_r": AngularDistance,
    }
)


def get(identifier: str | None) -> Observable | None:
    if identifier is None or identifier == "None":
        return

    else:
        return ALL_OBJECTS_DICT.get(identifier)


def register_observable(obs: Observable, *alias: str) -> None:
    ALL_OBJECTS.add(obs)

    for name in alias:
        ALL_OBJECTS_DICT[name] = obs


def parse_observable(name: str | None, **kwargs) -> Observable | None:
    if name is None or (isinstance(name, str) and name == "None"):
        return

    if (class_name := name.split(".")[-1]) in ALL_OBJECTS_DICT:
        kwargs["class_name"] = class_name
        return ALL_OBJECTS_DICT[class_name].from_name(name, **kwargs)

    elif re.match(r"^tau\d$", class_name.lower()):
        kwargs["class_name"] = class_name
        return TauN.from_name(name, **kwargs)

    elif re.match(r"^tau\d\d$", class_name.lower()):
        kwargs["class_name"] = class_name
        return TauMN.from_name(name, **kwargs)

    else:
        raise ValueError(f"Invalid '{name}' for an observable")
