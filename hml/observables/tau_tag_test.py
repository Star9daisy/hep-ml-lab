from math import isnan

import pytest

from ..events.delphes_events import DelphesEvents
from .tau_tag import TauTag


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_tau_tag(event):
    obs = TauTag(physics_object="FatJet0")
    assert obs.physics_object.name == "FatJet0"
    assert obs.supported_objects == ["single", "collective"]
    assert obs.name == "TauTag"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet0.TauTag"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "TauTag"
    assert obs.config == {
        "physics_object": "FatJet0",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective"],
    }
    assert TauTag.from_name("FatJet0.TauTag").fullname == obs.fullname
    assert TauTag.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, int)

    obs = TauTag(physics_object="FatJet:5")
    assert obs.physics_object.name == "FatJet:5"
    assert obs.supported_objects == ["single", "collective"]
    assert obs.name == "TauTag"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet:5.TauTag"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "TauTag"
    assert obs.config == {
        "physics_object": "FatJet:5",
        "name": None,
        "value": None,
        "supported_objects": ["single", "collective"],
    }
    assert TauTag.from_name("FatJet:5.TauTag").fullname == obs.fullname
    assert TauTag.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert len(obs.value) == 5


def test_bad_case(event):
    # Bad index
    assert isnan(TauTag(physics_object="FatJet100").read(event).value)

    # Bad start index
    assert TauTag(physics_object="FatJet100:").read(event).value == []
