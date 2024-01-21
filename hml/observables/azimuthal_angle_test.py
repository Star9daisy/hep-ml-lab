from math import isnan

import pytest

from hml.events import DelphesEvents
from hml.observables import AzimuthalAngle
from hml.observables import Phi


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_azimuthal_angle(event):
    obs = AzimuthalAngle(physics_object="FatJet0")
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_objects == ["single", "collective", "nested"]
    assert obs.name == "AzimuthalAngle"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet0.AzimuthalAngle"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "AzimuthalAngle"
    assert obs.config == {
        "physics_object": "FatJet0",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective", "nested"],
    }
    assert AzimuthalAngle.from_name("FatJet0.AzimuthalAngle").fullname == obs.fullname
    assert AzimuthalAngle.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, float)

    obs = AzimuthalAngle(physics_object="FatJet:5")
    obs.read(event)
    assert len(obs.value) == 5

    obs = AzimuthalAngle(physics_object="Jet:2.Particles:3")
    obs.read(event)
    assert len(obs.value) == 2
    assert len(obs.value[0]) == 3


def test_phi(event):
    obs = Phi(physics_object="FatJet0")
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_objects == ["single", "collective", "nested"]
    assert obs.name == "Phi"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet0.Phi"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "Phi"
    assert obs.config == {
        "physics_object": "FatJet0",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective", "nested"],
    }
    assert Phi.from_name("FatJet0.Phi").fullname == obs.fullname
    assert Phi.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, float)

    obs = Phi(physics_object="FatJet:5")
    obs.read(event)
    assert len(obs.value) == 5

    obs = Phi(physics_object="Jet:2.Particles:3")
    obs.read(event)
    assert len(obs.value) == 2
    assert len(obs.value[0]) == 3
