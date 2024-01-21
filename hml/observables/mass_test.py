from math import isnan

import pytest

from hml.events import DelphesEvents
from hml.observables import M
from hml.observables import Mass


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_mass(event):
    obs = Mass(physics_object="FatJet0")
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_objects == ["single", "collective", "nested"]
    assert obs.name == "Mass"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet0.Mass"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "Mass"
    assert obs.config == {
        "physics_object": "FatJet0",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective", "nested"],
    }
    assert Mass.from_name("FatJet0.Mass").fullname == obs.fullname
    assert Mass.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, float)

    obs = Mass(physics_object="FatJet:5")
    obs.read(event)
    assert len(obs.value) == 5

    obs = Mass(physics_object="Jet:2.Particles:3")
    obs.read(event)
    assert len(obs.value) == 2
    assert len(obs.value[0]) == 3


def test_m(event):
    obs = M(physics_object="FatJet0")
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_objects == ["single", "collective", "nested"]
    assert obs.name == "M"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet0.M"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "M"
    assert obs.config == {
        "physics_object": "FatJet0",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective", "nested"],
    }
    assert M.from_name("FatJet0.M").fullname == obs.fullname
    assert M.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, float)

    obs = M(physics_object="FatJet:5")
    obs.read(event)
    assert len(obs.value) == 5

    obs = M(physics_object="Jet:2.Particles:3")
    obs.read(event)
    assert len(obs.value) == 2
    assert len(obs.value[0]) == 3
