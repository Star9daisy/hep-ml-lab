from math import isnan

import pytest

from ..events.delphes_events import DelphesEvents
from .momentum_y import MomentumY
from .momentum_y import Py


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2zz/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_attributes():
    obs = MomentumY("Jet0")

    assert obs.physics_object.identifier == "Jet0"
    assert obs.supported_types == ["single", "collective", "nested"]
    assert obs.name == "MomentumY"
    assert isnan(obs.value)
    assert obs.dtype == "float64"

    assert obs.shape == "1 * float64"
    assert obs.identifier == "Jet0.MomentumY"
    assert obs.config == {
        "physics_object": obs.physics_object.identifier,
        "name": obs.name,
        "value": obs.value,
        "dtype": obs.dtype,
    }
    assert repr(obs) == "Jet0.MomentumY : nan"

    assert MomentumY.from_identifier("Jet0.MomentumY").config == obs.config

    obs = Py("Jet0")
    assert obs.name == "Py"
    assert obs.identifier == "Jet0.Py"


def test_read(event):
    obs = Py("Jet0").read(event)
    assert obs.shape == "1 * float64"

    obs = Py("Jet:5").read(event)
    assert obs.shape == "5 * float64"

    obs = Py("Jet:2.Constituents:5").read(event)
    assert obs.shape == "2 * 5 * float64"
