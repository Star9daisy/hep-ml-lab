from math import isnan

import pytest

from hml.events import DelphesEvents
from hml.observables import MomentumX
from hml.observables import Px


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_momentum_x(event):
    obs = MomentumX(physics_object="FatJet0")
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_objects == ["single", "collective", "nested"]
    assert obs.name == "MomentumX"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet0.MomentumX"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "MomentumX"
    assert obs.config == {
        "physics_object": "FatJet0",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective", "nested"],
    }
    assert MomentumX.from_name("FatJet0.MomentumX").fullname == obs.fullname
    assert MomentumX.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, float)

    obs = MomentumX(physics_object="FatJet:5")
    obs.read(event)
    assert len(obs.value) == 5

    obs = MomentumX(physics_object="Jet:2.Particles:3")
    obs.read(event)
    assert len(obs.value) == 2
    assert len(obs.value[0]) == 3


def test_px(event):
    obs = Px(physics_object="FatJet0")
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_objects == ["single", "collective", "nested"]
    assert obs.name == "Px"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet0.Px"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "Px"
    assert obs.config == {
        "physics_object": "FatJet0",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective", "nested"],
    }
    assert Px.from_name("FatJet0.Px").fullname == obs.fullname
    assert Px.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, float)

    obs = Px(physics_object="FatJet:5")
    obs.read(event)
    assert len(obs.value) == 5

    obs = Px(physics_object="Jet:2.Particles:3")
    obs.read(event)
    assert len(obs.value) == 2
    assert len(obs.value[0]) == 3
