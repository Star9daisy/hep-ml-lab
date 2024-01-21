from math import isnan

import pytest

from ..events.delphes_events import DelphesEvents
from .transverse_momentum import Pt
from .transverse_momentum import TransverseMomentum


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_transverse_momentum(event):
    obs = TransverseMomentum(physics_object="FatJet0")
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_objects == ["single", "collective", "nested"]
    assert obs.name == "TransverseMomentum"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet0.TransverseMomentum"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "TransverseMomentum"
    assert obs.config == {
        "physics_object": "FatJet0",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective", "nested"],
    }
    assert (
        TransverseMomentum.from_name("FatJet0.TransverseMomentum").fullname
        == obs.fullname
    )
    assert TransverseMomentum.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, float)

    obs = TransverseMomentum(physics_object="FatJet:5")
    obs.read(event)
    assert len(obs.value) == 5

    obs = TransverseMomentum(physics_object="Jet:2.Particles:3")
    obs.read(event)
    assert len(obs.value) == 2
    assert len(obs.value[0]) == 3


def test_pt(event):
    obs = Pt(physics_object="FatJet0")
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_objects == ["single", "collective", "nested"]
    assert obs.name == "Pt"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet0.Pt"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "Pt"
    assert obs.config == {
        "physics_object": "FatJet0",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective", "nested"],
    }
    assert Pt.from_name("FatJet0.Pt").fullname == obs.fullname
    assert Pt.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, float)

    obs = Pt(physics_object="FatJet:5")
    obs.read(event)
    assert len(obs.value) == 5

    obs = Pt(physics_object="Jet:2.Particles:3")
    obs.read(event)
    assert len(obs.value) == 2
    assert len(obs.value[0]) == 3


def test_bad_case(event):
    assert isnan(Pt(physics_object="FatJet100").read(event).value)
