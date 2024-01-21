from math import isnan

import pytest

from ..events.delphes_events import DelphesEvents
from .pseudo_rapidity import Eta
from .pseudo_rapidity import PseudoRapidity


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_pseudo_rapidity(event):
    obs = PseudoRapidity(physics_object="FatJet0")
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_objects == ["single", "collective", "nested"]
    assert obs.name == "PseudoRapidity"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet0.PseudoRapidity"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "PseudoRapidity"
    assert obs.config == {
        "physics_object": "FatJet0",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective", "nested"],
    }
    assert PseudoRapidity.from_name("FatJet0.PseudoRapidity").fullname == obs.fullname
    assert PseudoRapidity.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, float)

    obs = PseudoRapidity(physics_object="FatJet:5")
    obs.read(event)
    assert len(obs.value) == 5

    obs = PseudoRapidity(physics_object="Jet:2.Particles:3")
    obs.read(event)
    assert len(obs.value) == 2
    assert len(obs.value[0]) == 3


def test_eta(event):
    obs = Eta(physics_object="FatJet0")
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_objects == ["single", "collective", "nested"]
    assert obs.name == "Eta"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet0.Eta"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "Eta"
    assert obs.config == {
        "physics_object": "FatJet0",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective", "nested"],
    }
    assert Eta.from_name("FatJet0.Eta").fullname == obs.fullname
    assert Eta.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, float)

    obs = Eta(physics_object="FatJet:5")
    obs.read(event)
    assert len(obs.value) == 5

    obs = Eta(physics_object="Jet:2.Particles:3")
    obs.read(event)
    assert len(obs.value) == 2
    assert len(obs.value[0]) == 3


def test_bad_case(event):
    assert isnan(Eta(physics_object="FatJet100").read(event).value)
