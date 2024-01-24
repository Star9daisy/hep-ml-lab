from math import isnan

import pytest

from ..events.delphes_events import DelphesEvents
from .size import Size


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_attributes():
    obs = Size("FatJet:")

    assert obs.physics_object.identifier == "FatJet:"
    assert obs.supported_types == ["collective"]
    assert obs.name == "Size"
    assert isnan(obs.value)
    assert obs.dtype == "float64"

    assert obs.shape == "1 * float64"
    assert obs.identifier == "FatJet:.Size"
    assert obs.config == {
        "physics_object": obs.physics_object.identifier,
        "name": obs.name,
        "value": obs.value,
        "dtype": obs.dtype,
    }
    assert repr(obs) == "FatJet:.Size : nan"

    assert Size.from_identifier("FatJet:.Size").config == obs.config


def test_read(event):
    obs = Size("FatJet:").read(event)
    assert isinstance(obs.value, int)
    assert obs.shape == "1 * float64"

    obs = Size("FatJet:5").read(event)
    assert isinstance(obs.value, int)
    assert obs.shape == "1 * float64"
