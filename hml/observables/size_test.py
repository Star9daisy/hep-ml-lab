from math import isnan

import pytest

from hml.events import DelphesEvents
from hml.observables import Size


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_size(event):
    obs = Size(physics_object="FatJet")
    assert obs.physics_object.name == "FatJet"
    assert obs.supported_objects == ["collective"]
    assert obs.name == "Size"
    assert isnan(obs.value)
    assert obs.fullname == "FatJet.Size"
    assert repr(obs) == f"{obs.fullname}: {obs.value}"
    assert obs.classname == "Size"
    assert obs.config == {
        "physics_object": "FatJet",
        "name": None,
        "value": None,
        "supported_objects": ["collective"],
    }
    assert Size.from_name("FatJet.Size").fullname == obs.fullname
    assert Size.from_config(obs.config).fullname == obs.fullname

    obs.read(event)
    assert isinstance(obs.value, int)


def test_bad_case(event):
    # Not supported physics object
    with pytest.raises(TypeError):
        Size(physics_object="FatJet0")

    # Bad start index
    assert Size(physics_object="FatJet100:").read(event).value == 0
