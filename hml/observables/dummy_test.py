from math import isnan
from math import nan

import pytest

from ..events.delphes_events import DelphesEvents
from .dummy import Dummy


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_attributes():
    obs = Dummy()

    assert obs.physics_object is None
    assert obs.supported_types is None
    assert obs.name == "Dummy"
    assert isnan(obs.value)
    assert obs.dtype == "float64"

    assert obs.shape == "1 * float64"
    assert obs.identifier == "Dummy"
    assert obs.config == {
        "physics_object": None,
        "name": "Dummy",
        "value": nan,
        "dtype": "float64",
    }

    assert repr(obs) == "Dummy : nan"

    assert Dummy.from_identifier("Dummy").config == obs.config


def test_read(event):
    assert Dummy().read(event).value == [1]
