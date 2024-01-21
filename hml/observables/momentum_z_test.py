from math import isnan

import pytest

from hml.events import DelphesEvents
from hml.observables import MomentumZ
from hml.observables import Pz


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_momentum_z(event):
    obs = MomentumZ(physics_object="FatJet0")
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_objects == ["single", "collective", "nested"]
    assert obs.name == "MomentumZ"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet0.MomentumZ"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "MomentumZ"
    assert obs.config == {
        "physics_object": "FatJet0",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective", "nested"],
    }
    assert MomentumZ.from_name("FatJet0.MomentumZ").fullname == obs.fullname
    assert MomentumZ.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, float)

    obs = MomentumZ(physics_object="FatJet:5")
    obs.read(event)
    assert len(obs.value) == 5

    obs = MomentumZ(physics_object="Jet:2.Particles:3")
    obs.read(event)
    assert len(obs.value) == 2
    assert len(obs.value[0]) == 3


def test_pz(event):
    obs = Pz(physics_object="FatJet0")
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_objects == ["single", "collective", "nested"]
    assert obs.name == "Pz"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet0.Pz"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "Pz"
    assert obs.config == {
        "physics_object": "FatJet0",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective", "nested"],
    }
    assert Pz.from_name("FatJet0.Pz").fullname == obs.fullname
    assert Pz.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, float)

    obs = Pz(physics_object="FatJet:5")
    obs.read(event)
    assert len(obs.value) == 5

    obs = Pz(physics_object="Jet:2.Particles:3")
    obs.read(event)
    assert len(obs.value) == 2
    assert len(obs.value[0]) == 3
