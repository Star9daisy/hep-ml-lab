from math import isnan

import pytest

from ..events.delphes_events import DelphesEvents
from .tau_tag import TauTag


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_attributes():
    obs = TauTag("FatJet0")

    assert obs.physics_object.identifier == "FatJet0"
    assert obs.supported_types == ["single", "collective"]
    assert obs.name == "TauTag"
    assert isnan(obs.value)
    assert obs.dtype == "float64"

    assert obs.shape == "1 * float64"
    assert obs.identifier == "FatJet0.TauTag"
    assert obs.config == {
        "physics_object": obs.physics_object.identifier,
        "name": obs.name,
        "value": obs.value,
        "dtype": obs.dtype,
    }
    assert repr(obs) == "FatJet0.TauTag"

    assert TauTag.from_identifier("FatJet0.TauTag").config == obs.config


def test_read(event):
    obs = TauTag("FatJet0").read(event)
    assert isinstance(obs.value, float)
    assert obs.shape == "1 * float64"

    obs = TauTag("FatJet:5").read(event)
    assert isinstance(obs.value, list)
    assert obs.shape == "5 * float64"
