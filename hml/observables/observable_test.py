from math import isnan

import pytest

from hml.observables import Observable
from hml.observables import get


def test_observable():
    obs = Observable()
    assert obs.physics_object is None
    assert obs.supported_objects == ["all"]
    assert obs.name == "Observable"
    assert isnan(obs.value)
    assert obs.fullname == "Observable"
    assert obs.fullname == repr(obs)
    assert obs.classname == "Observable"
    assert obs.physics_object is None
    assert obs.config == {
        "physics_object": None,
        "name": None,
        "value": None,
        "supported_objects": "all",
    }
    assert Observable.from_name("Observable").fullname == obs.fullname
    assert Observable.from_config(obs.config).fullname == obs.fullname

    obs = Observable(physics_object="Jet")
    assert obs.physics_object.name == "Jet"
    assert obs.supported_objects == ["all"]
    assert obs.name == "Observable"
    assert isnan(obs.value)
    assert obs.fullname == "Jet.Observable"
    assert obs.fullname == repr(obs)
    assert obs.classname == "Observable"
    assert obs.physics_object.name == "Jet"
    assert obs.config == {
        "physics_object": "Jet",
        "name": None,
        "value": None,
        "supported_objects": "all",
    }
    assert Observable.from_name("Jet.Observable").fullname == obs.fullname
    assert Observable.from_config(obs.config).fullname == obs.fullname

    obs = Observable(physics_object="Jet", name="MyObservable")
    assert obs.physics_object.name == "Jet"
    assert obs.supported_objects == ["all"]
    assert obs.name == "MyObservable"
    assert isnan(obs.value)
    assert obs.fullname == "Jet.MyObservable"
    assert obs.fullname == repr(obs)
    assert obs.classname == "Observable"
    assert obs.physics_object.name == "Jet"
    assert obs.config == {
        "physics_object": "Jet",
        "name": "MyObservable",
        "value": None,
        "supported_objects": "all",
    }
    assert Observable.from_name("Jet.MyObservable").fullname == obs.fullname
    assert Observable.from_config(obs.config).fullname == obs.fullname

    obs = Observable(physics_object="Jet0", supported_objects=["single"])
    assert obs.supported_objects == ["single"]

    obs = Observable(physics_object="Jet", supported_objects=["collective"])
    obs = Observable(physics_object="Jet0.Particles", supported_objects=["nested"])
    obs = Observable(
        physics_object="Jet0,Jet1", supported_objects=["single", "multiple"]
    )

    obs = Observable(physics_object="Jet0", supported_objects=["single", "multiple"])
    obs._value = 0
    assert obs.value == 0


def test_bad_cases():
    with pytest.raises(TypeError):
        Observable(supported_objects=["single"])

    with pytest.raises(TypeError):
        Observable(physics_object="Jet0", supported_objects=["collective"])

    with pytest.raises(ValueError):
        Observable(physics_object="Jet0", supported_objects=["wrong support object"])


def test_get():
    assert get("") is None
    assert get(None) is None
    assert get("UnknownObservable") is None

    assert get("FatJet0.TauN", 1).fullname == "FatJet0.Tau1"
    assert get("FatJet0.tau_n", 1).fullname == "FatJet0.Tau1"
    assert get("FatJet0.tau_1").fullname == "FatJet0.Tau1"
    assert get("FatJet0.Tau1").fullname == "FatJet0.Tau1"
    assert get("FatJet0.tau1").fullname == "FatJet0.Tau1"

    assert get("FatJet0.TauMN", 2, 1).fullname == "FatJet0.Tau21"
    assert get("FatJet0.tau_mn", 2, 1).fullname == "FatJet0.Tau21"
    assert get("FatJet0.tau_21").fullname == "FatJet0.Tau21"
    assert get("FatJet0.Tau21").fullname == "FatJet0.Tau21"
    assert get("FatJet0.tau21").fullname == "FatJet0.Tau21"
