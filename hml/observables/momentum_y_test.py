from math import isnan

import pytest

from ..events.delphes_events import DelphesEvents
from ..observables.momentum_y import MomentumY
from ..observables.momentum_y import Py


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_momentum_y(event):
    obs = MomentumY(physics_object="FatJet0")
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_objects == ["single", "collective", "nested"]
    assert obs.name == "MomentumY"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet0.MomentumY"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "MomentumY"
    assert obs.config == {
        "physics_object": "FatJet0",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective", "nested"],
    }
    assert MomentumY.from_name("FatJet0.MomentumY").fullname == obs.fullname
    assert MomentumY.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, float)

    obs = MomentumY(physics_object="FatJet:5")
    obs.read(event)
    assert len(obs.value) == 5

    obs = MomentumY(physics_object="Jet:2.Particles:3")
    obs.read(event)
    assert len(obs.value) == 2
    assert len(obs.value[0]) == 3


def test_py(event):
    obs = Py(physics_object="FatJet0")
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_objects == ["single", "collective", "nested"]
    assert obs.name == "Py"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet0.Py"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "Py"
    assert obs.config == {
        "physics_object": "FatJet0",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective", "nested"],
    }
    assert Py.from_name("FatJet0.Py").fullname == obs.fullname
    assert Py.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, float)

    obs = Py(physics_object="FatJet:5")
    obs.read(event)
    assert len(obs.value) == 5

    obs = Py(physics_object="Jet:2.Particles:3")
    obs.read(event)
    assert len(obs.value) == 2
    assert len(obs.value[0]) == 3


def test_bad_case(event):
    assert isnan(Py(physics_object="FatJet100").read(event).value)
