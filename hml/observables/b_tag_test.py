from math import isnan

import pytest

from ..events.delphes_events import DelphesEvents
from .b_tag import BTag


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_attributes():
    obs = BTag("FatJet0")

    assert obs.physics_object.identifier == "FatJet0"
    assert obs.supported_types == ["single", "collective"]
    assert obs.name == "BTag"
    assert isnan(obs.value)
    assert obs.dtype == "float64"

    assert obs.shape == "1 * float64"
    assert obs.identifier == "FatJet0.BTag"
    assert obs.config == {
        "physics_object": obs.physics_object.identifier,
        "name": obs.name,
        "value": obs.value,
        "dtype": obs.dtype,
    }
    assert repr(obs) == "FatJet0.BTag"

    assert BTag.from_identifier("FatJet0.BTag").config == obs.config


def test_read(event):
    obs = BTag("FatJet0").read(event)
    assert obs.shape == "1 * float64"

    obs = BTag("FatJet:5").read(event)
    assert obs.shape == "5 * float64"
