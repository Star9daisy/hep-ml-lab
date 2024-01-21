from math import isnan

import pytest

from hml.events import DelphesEvents
from hml.observables import BTag


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_b_tag(event):
    obs = BTag(physics_object="FatJet0")
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_objects == ["single", "collective"]
    assert obs.name == "BTag"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet0.BTag"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "BTag"
    assert obs.config == {
        "physics_object": "FatJet0",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective"],
    }
    assert BTag.from_name("FatJet0.BTag").fullname == obs.fullname
    assert BTag.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, int)

    obs = BTag(physics_object="FatJet:5")
    assert obs.physics_object.name == "FatJet:5"
    assert obs.supported_objects == ["single", "collective"]
    assert obs.name == "BTag"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet:5.BTag"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "BTag"
    assert obs.config == {
        "physics_object": "FatJet:5",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective"],
    }
    assert BTag.from_name("FatJet:5.BTag").fullname == obs.fullname
    assert BTag.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert len(obs.value) == 5


def test_bad_case(event):
    # Bad index
    assert isnan(BTag(physics_object="FatJet100").read(event).value)

    # Bad start index
    assert BTag(physics_object="FatJet100:").read(event).value == []
