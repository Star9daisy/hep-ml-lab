from math import isnan

import pytest

from ..events.delphes_events import DelphesEvents
from ..observables.charge import Charge


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_b_tag(event):
    obs = Charge(physics_object="FatJet0")
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_objects == ["single", "collective"]
    assert obs.name == "Charge"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet0.Charge"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "Charge"
    assert obs.config == {
        "physics_object": "FatJet0",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective"],
    }
    assert Charge.from_name("FatJet0.Charge").fullname == obs.fullname
    assert Charge.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, int)

    obs = Charge(physics_object="FatJet:5")
    assert obs.physics_object.name == "FatJet:5"
    assert obs.supported_objects == ["single", "collective"]
    assert obs.name == "Charge"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet:5.Charge"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "Charge"
    assert obs.config == {
        "physics_object": "FatJet:5",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective"],
    }
    assert Charge.from_name("FatJet:5.Charge").fullname == obs.fullname
    assert Charge.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert len(obs.value) == 5


def test_bad_case(event):
    # Bad index
    assert isnan(Charge(physics_object="FatJet100").read(event).value)

    # Bad start index
    assert Charge(physics_object="FatJet100:").read(event).value == []
