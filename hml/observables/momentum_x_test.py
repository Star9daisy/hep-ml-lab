from math import isnan

import pytest

from ..events.delphes_events import DelphesEvents
from .momentum_x import MomentumX
from .momentum_x import Px


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_attributes():
    obs = MomentumX("Jet0")

    assert obs.physics_object.identifier == "Jet0"
    assert obs.supported_types == ["single", "collective", "nested"]
    assert obs.name == "MomentumX"
    assert isnan(obs.value)
    assert obs.dtype == "float64"

    assert obs.shape == "1 * float64"
    assert obs.identifier == "Jet0.MomentumX"
    assert obs.config == {
        "physics_object": obs.physics_object.identifier,
        "name": obs.name,
        "value": obs.value,
        "dtype": obs.dtype,
    }
    assert repr(obs) == "Jet0.MomentumX : nan"

    assert MomentumX.from_identifier("Jet0.MomentumX").config == obs.config

    obs = Px("Jet0")
    assert obs.name == "Px"
    assert obs.identifier == "Jet0.Px"


def test_read(event):
    obs = Px("Jet0").read(event)
    assert obs.shape == "1 * float64"

    obs = Px("Jet:5").read(event)
    assert obs.shape == "5 * float64"

    obs = Px("Jet:2.Constituents:5").read(event)
    assert obs.shape == "2 * 5 * float64"
