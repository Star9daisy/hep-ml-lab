from math import isnan

import pytest

from hml.events import DelphesEvents
from hml.observables import E
from hml.observables import Energy


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_energy(event):
    obs = Energy(physics_object="FatJet0")
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_objects == ["single", "collective", "nested"]
    assert obs.name == "Energy"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet0.Energy"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "Energy"
    assert obs.config == {
        "physics_object": "FatJet0",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective", "nested"],
    }
    assert Energy.from_name("FatJet0.Energy").fullname == obs.fullname
    assert Energy.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, float)

    obs = Energy(physics_object="FatJet:5")
    obs.read(event)
    assert len(obs.value) == 5

    obs = Energy(physics_object="Jet:2.Particles:3")
    obs.read(event)
    assert len(obs.value) == 2
    assert len(obs.value[0]) == 3


def test_e(event):
    obs = E(physics_object="FatJet0")
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_objects == ["single", "collective", "nested"]
    assert obs.name == "E"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet0.E"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "E"
    assert obs.config == {
        "physics_object": "FatJet0",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective", "nested"],
    }
    assert E.from_name("FatJet0.E").fullname == obs.fullname
    assert E.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, float)

    obs = E(physics_object="FatJet:5")
    obs.read(event)
    assert len(obs.value) == 5

    obs = E(physics_object="Jet:2.Particles:3")
    obs.read(event)
    assert len(obs.value) == 2
    assert len(obs.value[0]) == 3
